# -*- coding: utf-8 -*-
"""
KPI JSON の検算（ダブルチェック）
--------------------------------
KPI JSON の "verify" に書いた検算式を実行し、シート記載値と一致するかを判定する。
build_kpi.py からも呼ばれ、結果はダッシュボードの「検算・ダブルチェック結果」に載る。

verify の書式:
  {"name": "説明", "op": "sum|avg|div|sub", "values": [...], "expected": 数値,
   "tol": 許容誤差(既定1), "scale": 倍率(div のみ・既定1)}
    sum : values の合計
    avg : values の平均
    div : values[0] / values[1] * scale
    sub : values[0] - values[1]

使い方:
    python verify_kpi.py <kpi.json>     # 不一致が1件でもあれば終了コード1
"""
import sys
import json


def compute(chk):
    v = chk['values']
    op = chk.get('op', 'sum')
    if op == 'sum':
        return float(sum(v))
    if op == 'avg':
        return float(sum(v)) / len(v)
    if op == 'div':
        return float(v[0]) / float(v[1]) * chk.get('scale', 1)
    if op == 'sub':
        return float(v[0]) - float(v[1])
    raise ValueError(f'unknown op: {op}')


def run_checks(checks):
    results = []
    for chk in checks:
        got = compute(chk)
        exp = chk['expected']
        ok = abs(got - exp) <= chk.get('tol', 1)
        results.append({'name': chk['name'], 'computed': got, 'expected': exp, 'ok': ok})
    return results


def fmt(x):
    return f'{x:,.0f}' if abs(x) >= 100 else f'{x:,.2f}'


def main():
    if len(sys.argv) < 2:
        print('usage: python verify_kpi.py <kpi.json>')
        sys.exit(2)
    with open(sys.argv[1], encoding='utf-8') as f:
        data = json.load(f)
    res = run_checks(data.get('verify', []))
    for r in res:
        mark = 'OK ' if r['ok'] else 'NG!'
        print(f"[{mark}] {r['name']}: 計算 {fmt(r['computed'])} / 記載 {fmt(r['expected'])}")
    ng = [r for r in res if not r['ok']]
    print(f'--- {len(res)}件中 一致 {len(res) - len(ng)}件 / 不一致 {len(ng)}件')
    sys.exit(1 if ng else 0)


if __name__ == '__main__':
    main()
