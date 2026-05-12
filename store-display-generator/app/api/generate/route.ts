import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import { toFile } from "openai/uploads";
import { buildEditPrompt } from "@/lib/prompt";

export const runtime = "nodejs";
export const maxDuration = 120;

type SupportedSize = "1024x1024" | "1536x1024" | "1024x1536";

const ALLOWED_SIZES: SupportedSize[] = ["1024x1024", "1536x1024", "1024x1536"];

export async function POST(req: NextRequest) {
  try {
    const form = await req.formData();
    const shelf = form.get("shelf");
    const mask = form.get("mask");
    const products = form.getAll("products");
    const instructions = String(form.get("instructions") ?? "");
    const sizeInput = String(form.get("size") ?? "1024x1024") as SupportedSize;
    const size: SupportedSize = ALLOWED_SIZES.includes(sizeInput)
      ? sizeInput
      : "1024x1024";

    if (!(shelf instanceof Blob)) {
      return NextResponse.json(
        { error: "shelf image is required" },
        { status: 400 },
      );
    }
    if (!(mask instanceof Blob)) {
      return NextResponse.json(
        { error: "mask image is required" },
        { status: 400 },
      );
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return NextResponse.json(
        { error: "OPENAI_API_KEY is not set" },
        { status: 500 },
      );
    }

    const client = new OpenAI({ apiKey });

    const shelfFile = await toFile(shelf, "shelf.png", { type: "image/png" });
    const maskFile = await toFile(mask, "mask.png", { type: "image/png" });
    const productFiles = await Promise.all(
      products
        .filter((p): p is Blob => p instanceof Blob)
        .map((p, i) =>
          toFile(p, `product-${i}.png`, { type: "image/png" }),
        ),
    );

    const imageInput =
      productFiles.length > 0 ? [shelfFile, ...productFiles] : shelfFile;

    const result = await client.images.edit({
      model: "gpt-image-1",
      image: imageInput,
      mask: maskFile,
      prompt: buildEditPrompt(instructions),
      size,
      n: 1,
    });

    const b64 = result.data?.[0]?.b64_json;
    if (!b64) {
      return NextResponse.json(
        { error: "no image returned from model" },
        { status: 502 },
      );
    }

    return NextResponse.json({ b64 });
  } catch (err) {
    const message = err instanceof Error ? err.message : "unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
