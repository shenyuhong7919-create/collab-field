#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 palettes.html：12 张配色卡片 + 打开光场链接。"""
import io, os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(io.open(os.path.join(BASE, "data", "palettes.json"), encoding="utf-8"))

def ink(hexc):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#07060B" if (0.2126*r + 0.7152*g + 0.0722*b) > 152 else "#F6F3EE"

cards = []
for it in d["幕配色"]:
    n = it["序号"]
    main = '<span class="main">主入口</span>' if n == 9 else ''
    href = "index.html" if n == 9 else f"collab-{n:02d}.html"
    cards.append(f'''<a class="card" href="{href}" style="--c0:{it["c0"]};--hi:{it["hi"]};--fil:{it["fil"]};--ink:{ink(it["c0"])}">
  <div class="band"><b>{n:02d}</b><span class="pal">PAL</span><em>{it["en"]}</em></div>
  <div class="strip"><i style="background:{it["hi"]}"></i><i style="background:{it["fil"]}"></i></div>
  <div class="body">
    <h3>{it["用例"]}{main}</h3>
    <div class="hex"><span><s style="background:{it["c0"]}"></s>c0 {it["c0"]}</span><span><s style="background:{it["hi"]}"></s>hi {it["hi"]}</span><span><s style="background:{it["fil"]}"></s>fil {it["fil"]}</span></div>
    <div class="open">打开光场 →</div>
  </div>
</a>''')

html = f'''<!DOCTYPE html>
<!--
  COLLAB FIELD / 协作光场 — 一只黄学长, 2026
  Palette reference: ION 离子回路 / agent-display v8.0 theme 08
  Copyright (c) 2026 赛博老爸. PolyForm Noncommercial 1.0.0.
  Required Notice: Copyright (c) 2026 赛博老爸
  The palette cards and linked demo pages use synthetic data.
-->
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>十二幕配色 · 总览</title>
<style>
  :root{{--bg:#07060B;--panel:#0B0911;--line:#1A1823;--line2:#383546;
    --text:#ECE8F6;--dim:#A49FB6;--faint:#69647C;--white:#fff;
    --mono:"SF Mono",Menlo,Consolas,monospace;--sans:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:var(--bg);color:var(--text);font-family:var(--sans);-webkit-font-smoothing:antialiased}}
  body::before{{content:"";position:fixed;inset:0;pointer-events:none;
    background:radial-gradient(900px 520px at 12% -10%,rgba(157,180,255,.10),transparent 60%),
               radial-gradient(800px 460px at 92% 0%,rgba(255,143,214,.07),transparent 62%)}}
  .wrap{{position:relative;max-width:1280px;margin:0 auto;padding:46px 40px 36px}}
  .top{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--line2);padding-bottom:16px}}
  .eyebrow{{font:10px/1 var(--mono);letter-spacing:.24em;color:#9DB4FF;margin-bottom:10px}}
  h1{{font:600 34px/1.15 var(--sans);letter-spacing:.05em;color:var(--white)}}
  h1 em{{font-style:normal;color:#9DB4FF}}
  .sub{{font:11px/1.8 var(--mono);color:var(--dim);margin-top:8px}}
  .meta{{text-align:right;font:10px/1.9 var(--mono);color:var(--faint)}}
  .meta b{{display:block;font:600 26px/1 var(--mono);color:var(--white);margin-bottom:4px}}
  .legend{{display:flex;gap:22px;align-items:center;margin:16px 0 18px;font:10px/1.5 var(--sans);color:var(--faint)}}
  .legend b{{color:var(--dim);font-weight:500}}
  .legend s{{display:inline-block;width:9px;height:9px;margin-right:5px;vertical-align:-1px}}
  .legend .sp{{margin-left:auto;font-family:var(--mono);font-size:9px;letter-spacing:.08em}}
  .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}
  .card{{display:block;text-decoration:none;color:inherit;background:var(--panel);
    border:1px solid var(--line);transition:border-color .18s,transform .18s,box-shadow .18s;overflow:hidden}}
  .card:hover{{border-color:var(--c0);transform:translateY(-2px);box-shadow:0 12px 28px rgba(0,0,0,.4)}}
  .band{{position:relative;height:82px;background:var(--c0);color:var(--ink);padding:9px 11px}}
  .band b{{font:600 27px/1 var(--mono);letter-spacing:.02em}}
  .band .pal{{position:absolute;right:11px;top:10px;font:8px/1 var(--mono);letter-spacing:.16em;opacity:.7}}
  .band em{{position:absolute;left:11px;bottom:8px;font:8px/1 var(--mono);font-style:normal;letter-spacing:.12em;opacity:.75}}
  .strip{{display:flex;height:12px}}
  .strip i{{display:block;height:100%}}
  .strip i:first-child{{width:62%}}
  .strip i:last-child{{width:38%}}
  .body{{padding:11px 12px 12px}}
  .body h3{{font:600 15px/1.3 var(--sans);color:var(--white);display:flex;align-items:center;gap:7px}}
  .main{{font:8px/1 var(--mono);color:var(--c0);border:1px solid var(--c0);padding:2px 4px;letter-spacing:.06em}}
  .hex{{margin:8px 0 9px;display:grid;gap:2px}}
  .hex span{{font:8.5px/1.5 var(--mono);color:var(--dim);display:flex;align-items:center}}
  .hex s{{width:7px;height:7px;margin-right:5px;display:inline-block;border:1px solid rgba(255,255,255,.14)}}
  .open{{font:8.5px/1 var(--mono);color:var(--c0);letter-spacing:.06em}}
  footer{{display:flex;justify-content:space-between;gap:20px;margin-top:22px;border-top:1px solid var(--line);padding-top:12px;
    font:8.5px/1.7 var(--mono);color:var(--faint)}}
  footer a{{color:var(--dim);text-decoration:none;border-bottom:1px solid var(--line2)}}
  footer b{{color:var(--dim);font-weight:500}}
  @media (max-width:1100px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div>
      <div class="eyebrow">PALETTE INDEX / 12 SCENES</div>
      <h1>十二幕 · <em>配色总览</em></h1>
      <div class="sub">12 套 c0 / hi / fil · 协作光场同系列材料 · 合成演示数据 · by 一只黄学长</div>
    </div>
    <div class="meta"><b>12 / 12</b>PALETTES · CLICK TO OPEN</div>
  </div>

  <div class="legend">
    <span><s style="background:#18C8FF"></s><b>c0</b> 主线网 / 面板 / 大面积色块</span>
    <span><s style="background:#A8F0FF"></s><b>hi</b> 点亮节点 / 路径光带 / 读数</span>
    <span><s style="background:#FFE066"></s><b>fil</b> 细丝高光 / 火花 / 辅助线</span>
    <span class="sp">c0 : hi : fil</span>
  </div>

  <div class="grid">
    {"".join(cards)}
  </div>

  <footer>
    <span>主入口 <b>09 综合总览</b>（金色）· <a href="index.html">index.html</a></span>
    <span>视觉参考 HALOFLUX · 配色参考 ION 离子回路 / agent-display 主题 08 · <b>PolyForm Noncommercial 1.0.0</b> · 仅限非商用</span>
  </footer>
</div>
</body>
</html>
'''
io.open(os.path.join(BASE, "palettes.html"), "w", encoding="utf-8").write(html)
print("palettes.html", len(html.encode()) // 1024, "KB")
