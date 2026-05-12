"use client";

import { useEffect, useRef, useState } from "react";

const TARGET_SIZE = 1024;

export default function Home() {
  const [shelfFile, setShelfFile] = useState<File | null>(null);
  const [productFiles, setProductFiles] = useState<File[]>([]);
  const [instructions, setInstructions] = useState(
    "Place the reference products on the middle shelf. 2 facings of product 1 on the left, 1 facing of product 2 on the right.",
  );
  const [resultB64, setResultB64] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [brushSize, setBrushSize] = useState(80);

  const shelfCanvasRef = useRef<HTMLCanvasElement>(null);
  const paintCanvasRef = useRef<HTMLCanvasElement>(null);
  const drawing = useRef(false);

  useEffect(() => {
    if (!shelfFile) return;
    const url = URL.createObjectURL(shelfFile);
    const img = new Image();
    img.onload = () => {
      const shelf = shelfCanvasRef.current;
      const paint = paintCanvasRef.current;
      if (!shelf || !paint) return;
      shelf.width = TARGET_SIZE;
      shelf.height = TARGET_SIZE;
      paint.width = TARGET_SIZE;
      paint.height = TARGET_SIZE;

      const sctx = shelf.getContext("2d");
      const pctx = paint.getContext("2d");
      if (!sctx || !pctx) return;

      const scale = Math.max(
        TARGET_SIZE / img.width,
        TARGET_SIZE / img.height,
      );
      const drawW = img.width * scale;
      const drawH = img.height * scale;
      sctx.fillStyle = "#000";
      sctx.fillRect(0, 0, TARGET_SIZE, TARGET_SIZE);
      sctx.drawImage(
        img,
        (TARGET_SIZE - drawW) / 2,
        (TARGET_SIZE - drawH) / 2,
        drawW,
        drawH,
      );

      pctx.clearRect(0, 0, TARGET_SIZE, TARGET_SIZE);

      URL.revokeObjectURL(url);
    };
    img.src = url;
  }, [shelfFile]);

  function canvasPoint(e: React.PointerEvent<HTMLCanvasElement>) {
    const canvas = paintCanvasRef.current;
    if (!canvas) return null;
    const rect = canvas.getBoundingClientRect();
    return {
      x: ((e.clientX - rect.left) / rect.width) * canvas.width,
      y: ((e.clientY - rect.top) / rect.height) * canvas.height,
    };
  }

  function paintAt(x: number, y: number) {
    const paint = paintCanvasRef.current;
    if (!paint) return;
    const ctx = paint.getContext("2d");
    if (!ctx) return;
    ctx.fillStyle = "rgba(239, 68, 68, 0.55)";
    ctx.beginPath();
    ctx.arc(x, y, brushSize, 0, Math.PI * 2);
    ctx.fill();
  }

  function clearPaint() {
    const paint = paintCanvasRef.current;
    if (!paint) return;
    const ctx = paint.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, paint.width, paint.height);
  }

  function onPointerDown(e: React.PointerEvent<HTMLCanvasElement>) {
    drawing.current = true;
    e.currentTarget.setPointerCapture(e.pointerId);
    const p = canvasPoint(e);
    if (p) paintAt(p.x, p.y);
  }
  function onPointerMove(e: React.PointerEvent<HTMLCanvasElement>) {
    if (!drawing.current) return;
    const p = canvasPoint(e);
    if (p) paintAt(p.x, p.y);
  }
  function onPointerUp(e: React.PointerEvent<HTMLCanvasElement>) {
    drawing.current = false;
    e.currentTarget.releasePointerCapture(e.pointerId);
  }

  async function canvasToPngBlob(canvas: HTMLCanvasElement): Promise<Blob> {
    return new Promise((resolve, reject) => {
      canvas.toBlob(
        (b) => (b ? resolve(b) : reject(new Error("canvas toBlob failed"))),
        "image/png",
      );
    });
  }

  function buildMaskBlob(): Promise<Blob> {
    const paint = paintCanvasRef.current;
    if (!paint) throw new Error("paint canvas missing");
    const out = document.createElement("canvas");
    out.width = paint.width;
    out.height = paint.height;
    const octx = out.getContext("2d");
    if (!octx) throw new Error("no 2d context");

    const pctx = paint.getContext("2d");
    if (!pctx) throw new Error("no paint context");
    const src = pctx.getImageData(0, 0, paint.width, paint.height);
    const dst = octx.createImageData(paint.width, paint.height);

    for (let i = 0; i < src.data.length; i += 4) {
      const painted = src.data[i + 3] > 0;
      if (painted) {
        dst.data[i + 0] = 0;
        dst.data[i + 1] = 0;
        dst.data[i + 2] = 0;
        dst.data[i + 3] = 0;
      } else {
        dst.data[i + 0] = 0;
        dst.data[i + 1] = 0;
        dst.data[i + 2] = 0;
        dst.data[i + 3] = 255;
      }
    }
    octx.putImageData(dst, 0, 0);
    return canvasToPngBlob(out);
  }

  async function generate() {
    if (!shelfCanvasRef.current || !paintCanvasRef.current) return;
    if (!shelfFile) {
      setError("売り場画像をアップロードしてください");
      return;
    }
    setLoading(true);
    setError(null);
    setResultB64(null);
    try {
      const shelfBlob = await canvasToPngBlob(shelfCanvasRef.current);
      const maskBlob = await buildMaskBlob();

      const form = new FormData();
      form.append("shelf", shelfBlob, "shelf.png");
      form.append("mask", maskBlob, "mask.png");
      form.append("instructions", instructions);
      form.append("size", "1024x1024");
      productFiles.forEach((f, i) => {
        form.append("products", f, `product-${i}.png`);
      });

      const res = await fetch("/api/generate", { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `HTTP ${res.status}`);
      setResultB64(data.b64);
    } catch (e) {
      setError(e instanceof Error ? e.message : "unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">売り場ジェネレーター</h1>
        <p className="text-sm text-neutral-600">
          冷凍ケースの現状写真と新商品画像から、配置イメージを生成します。
        </p>
      </header>

      <section className="space-y-6">
        <div className="rounded-lg border border-neutral-200 bg-white p-4">
          <h2 className="mb-2 font-semibold">1. 売り場の写真</h2>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setShelfFile(e.target.files?.[0] ?? null)}
            className="block w-full text-sm"
          />
          <p className="mt-1 text-xs text-neutral-500">
            真正面・正方形に近い構図で撮影してください(1024×1024に中央クロップされます)。
          </p>
        </div>

        <div className="rounded-lg border border-neutral-200 bg-white p-4">
          <h2 className="mb-2 font-semibold">2. 新商品の画像(複数可)</h2>
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={(e) =>
              setProductFiles(Array.from(e.target.files ?? []))
            }
            className="block w-full text-sm"
          />
          {productFiles.length > 0 && (
            <div className="mt-3 flex gap-2 overflow-x-auto">
              {productFiles.map((f, i) => (
                <img
                  key={i}
                  src={URL.createObjectURL(f)}
                  alt={`product ${i + 1}`}
                  className="h-20 w-20 rounded border border-neutral-200 object-cover"
                />
              ))}
            </div>
          )}
        </div>

        <div className="rounded-lg border border-neutral-200 bg-white p-4">
          <h2 className="mb-2 font-semibold">
            3. 置く場所をなぞる(赤色エリアが差し替え対象)
          </h2>
          <div className="mb-2 flex items-center gap-3">
            <label className="text-sm">
              ブラシ:
              <input
                type="range"
                min={20}
                max={200}
                value={brushSize}
                onChange={(e) => setBrushSize(Number(e.target.value))}
                className="ml-2 align-middle"
              />
              <span className="ml-1 text-xs text-neutral-500">
                {brushSize}px
              </span>
            </label>
            <button
              type="button"
              onClick={clearPaint}
              className="rounded border border-neutral-300 px-3 py-1 text-sm hover:bg-neutral-100"
            >
              マスクをクリア
            </button>
          </div>
          <div className="relative mx-auto aspect-square w-full max-w-xl overflow-hidden rounded border border-neutral-300 bg-neutral-100">
            <canvas
              ref={shelfCanvasRef}
              className="absolute inset-0 h-full w-full"
            />
            <canvas
              ref={paintCanvasRef}
              onPointerDown={onPointerDown}
              onPointerMove={onPointerMove}
              onPointerUp={onPointerUp}
              onPointerCancel={onPointerUp}
              className="absolute inset-0 h-full w-full cursor-crosshair touch-none"
            />
          </div>
          <p className="mt-1 text-xs text-neutral-500">
            指/マウスでなぞった範囲が「ここを差し替えて」という指示になります。
          </p>
        </div>

        <div className="rounded-lg border border-neutral-200 bg-white p-4">
          <h2 className="mb-2 font-semibold">4. 配置の指示(英語推奨)</h2>
          <textarea
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            rows={4}
            className="w-full rounded border border-neutral-300 p-2 text-sm"
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={generate}
            disabled={loading || !shelfFile}
            className="rounded bg-emerald-600 px-6 py-2 font-semibold text-white shadow hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-neutral-300"
          >
            {loading ? "生成中..." : "売り場イメージを生成"}
          </button>
          {error && <span className="text-sm text-red-600">{error}</span>}
        </div>

        {resultB64 && (
          <div className="rounded-lg border border-neutral-200 bg-white p-4">
            <h2 className="mb-2 font-semibold">生成結果</h2>
            <img
              src={`data:image/png;base64,${resultB64}`}
              alt="generated display"
              className="mx-auto block max-w-xl rounded border border-neutral-300"
            />
            <p className="mt-2 text-center text-xs text-neutral-500">
              ※ これはシミュレーション画像です。実商品の細部と異なる場合があります。
            </p>
            <div className="mt-2 text-center">
              <a
                href={`data:image/png;base64,${resultB64}`}
                download="display.png"
                className="text-sm text-emerald-700 underline"
              >
                画像をダウンロード
              </a>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
