#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公开版构建器：HALOFLUX 源文件 + 合成数据 + 12 套配色。

COLLAB FIELD / 协作光场 — 一只黄学长，2026。

数据、配色、侧栏模板、上游源文件都在本目录内；不读取任何 vault / 本机路径。
输出：仓库根目录 collab-01..12.html + index.html。
"""
import io, os, re, json, colorsys, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "src", "haloflux-lab.html")
PALJSON = os.path.join(BASE, "data", "palettes.json")
DATAJSON = os.path.join(BASE, "data", "demo-network.json")
TPL = os.path.join(BASE, "src", "sidebar.tpl")

# ---------------------------------------------------------------------------
# ION 冷中性映射（与个人版一致）
# ---------------------------------------------------------------------------
NEU = [
    (0.00, (7, 6, 11)), (0.05, (10, 9, 16)), (0.10, (14, 11, 21)),
    (0.16, (26, 24, 35)), (0.24, (38, 34, 52)), (0.34, (56, 51, 74)),
    (0.45, (105, 100, 124)), (0.58, (132, 127, 149)), (0.63, (164, 159, 182)),
    (0.72, (201, 195, 217)), (0.83, (236, 232, 246)), (0.96, (255, 255, 255)),
]

def hx2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))

def neutral(l, hi):
    l = max(0.0, min(1.0, l))
    for i in range(len(NEU) - 1):
        l0, c0 = NEU[i]
        l1, c1 = NEU[i + 1]
        if l0 <= l <= l1:
            c = mix(c0, c1, (l - l0) / (l1 - l0)) if l1 > l0 else c0
            break
    else:
        c = NEU[-1][1]
    if l > 0.78:
        t = min(0.18, (l - 0.78) * 1.3)
        c = mix(c, hi, t)
    return c

def role_color(base, s, l, kind):
    br, bg, bb = hx2rgb(base)
    h, tl, ts = colorsys.rgb_to_hls(br / 255, bg / 255, bb / 255)
    if kind == 'c0':
        s2, l2 = min(0.95, 0.60 + s * 0.45), min(0.92, l * 0.96 + 0.04)
    elif kind == 'hi':
        s2, l2 = min(0.88, 0.46 + s * 0.42), min(0.84, l * 0.94)
    elif kind == 'warn':
        s2, l2 = min(0.90, 0.55 + s * 0.35), min(0.84, l * 0.90 + 0.06)
    else:
        s2, l2 = min(0.96, 0.58 + s * 0.40), min(0.88, l * 0.95 + 0.02)
    s2 = s2 * 0.80 + ts * 0.20
    l2 = l2 * 0.80 + tl * 0.20
    r, g, b = colorsys.hls_to_rgb(h, l2, s2)
    return round(r * 255), round(g * 255), round(b * 255)

def ion(r, g, b, pal, side=False, boost=False):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hi = hx2rgb(pal['hi'])
    hh, hl, hs = colorsys.rgb_to_hls(*[x / 255 for x in hi])
    hi_is_neutral = (hs < 0.15 and hl > 0.90)
    if l <= 0.10:
        return neutral(l, hi)
    if l >= 0.82:
        if boost:
            c0 = hx2rgb(pal['c0'])
            if (r, g, b) == (255, 255, 255):
                return mix((255, 255, 255), c0, 0.55)
            bh, bl, bs = colorsys.rgb_to_hls(*[x / 255 for x in c0])
            nl = 0.45 + 0.32 * min(1.0, max(0.0, (l - 0.82) / 0.18))
            ns = max(0.60, bs * 0.85)
            r2, g2, b2 = colorsys.hls_to_rgb(bh, nl, ns)
            return round(r2 * 255), round(g2 * 255), round(b2 * 255)
        return neutral(l, hi)
    if s <= (0.45 if side else 0.30):
        c = neutral(l, hi)
        if not side and 0.12 < l < 0.80:
            t = 0.22 * max(0.0, 1 - abs(l - 0.5) / 0.36)
            c = mix(c, hx2rgb(pal['c0']), t)
        return c
    if side:
        if 0.10 <= h <= 0.17:
            base, kind = pal['c0'], 'c0'
        elif 0.03 <= h < 0.10:
            base, kind = pal['fil'], 'fil'
        elif h >= 0.95 or h < 0.03:
            base, kind = pal['warn'], 'warn'
        else:
            return neutral(l, hi)
    else:
        if 0.40 <= h <= 0.56:
            base, kind = pal['c0'], 'c0'
        elif 0.60 <= h <= 0.85:
            base, kind = (pal['c0'], 'c0') if hi_is_neutral else (pal['hi'], 'hi')
        else:
            base, kind = pal['fil'], 'fil'
    return role_color(base, s, l, kind)

def colorize(s, pal=None, side=False, boost=False):
    def sub(m):
        v = m.group(0)[1:]
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        r, g, b = int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)
        r, g, b = ion(r, g, b, pal, side, boost)
        return "#%02x%02x%02x" % (r, g, b)
    def rgbasub(m):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        r, g, b = ion(r, g, b, pal, side, boost)
        return f"rgba({r},{g},{b}"
    s = re.sub(r"#[0-9a-fA-F]{6}\b", sub, s)
    s = re.sub(r"rgba\((\d{1,3}), ?(\d{1,3}), ?(\d{1,3})", rgbasub, s)
    if boost and pal:
        wc = "#%02x%02x%02x" % ion(255, 255, 255, pal, side, boost)
        s = s.replace("'#fff'", f"'{wc}'")
    return s

# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------
data = json.load(io.open(DATAJSON, encoding="utf-8"))
tasks, C = data["tasks"], data["counters"]
SHORT = data["secShort"]
seccount = data["sectorCount"]
secs = sorted(seccount.items(), key=lambda x: -x[1])
assert len(tasks) == C["tasks"], "counters.tasks 与 tasks 数量不一致"
assert len(data["tools"]) == C["tools"], "counters.tools 与 tools 数量不一致"
assert len(seccount) == C["sectors"] and sum(seccount.values()) == len(tasks), "sectorCount 与任务数不一致"
assert len(SHORT) == len(seccount), "secShort 与 sectorCount 不一致"

def q(s, n=26):
    s = s.replace("`", "").replace("'", "’").replace("\\", "/")
    return s if len(s) <= n else s[:n-1] + "…"

acts = [q(t["title"]) for t in tasks[-16:]]
acts_js = "const ACTS = [" + ",\n  ".join("'" + a + "'" for a in acts) + "];"
head = [f"{SHORT[s]} {n}" for s, n in secs] + [
    f"TASK {C['tasks']}", f"WORKSTREAM {C['sectors']}", f"TOOL {C['tools']}",
    f"GAP {C['gaps']}", f"PROOF {C['proof']}/{C['proofTotal']}",
    "BUILD", "ARCHIVE", "VERIFY", "LOG", "DATA"]
head_js = "const HEAD = [" + ", ".join("'" + h + "'" for h in head) + "];"
keys_js = "const KEYS = ['rows', 'tasks', 'tools', 'gaps', 'sects', 'creds', 'depth', 'date', 'ids', 'rate', 'bytes', 'ev', 'src', 'seed'];"
top = sorted(((t["name"], sum(1 for x in tasks if x["tool"] == t["name"])) for t in data["tools"]),
             key=lambda x: -x[1])[:5]
other = C["tools"] - len(top)
sample_sector = SHORT[secs[0][0]]
sample_tool = top[0][0]
sample_rows = next((t["rows"] for t in tasks if t["ev"] == "session"), 418)
code_t_js = ("const CODE_T = ['parse()', 'group()', 'emit()', 'hash', 'ok', 'PASS', "
             f"'{C['tasks']-2}/{C['tasks']}', 'task#{C['tasks']-1}', 'workstream', 'tool',"
             f" 'gap={C['gaps']}', 'proof={C['proof']}', 'rows', 'json', 'build', 'data', '->', '==', 'read', 'push', 'meta', 'probe', 'verify', 'done', 'log'];")
tok_js = ("const TOK = ['parse_spec()', "
          f"'task#{C['tasks']}', 'workstream={sample_sector}', 'tool={sample_tool}', 'rows={sample_rows}', "
          f"'gap={C['gaps']}', 'proof={C['proof']}/{C['proofTotal']}', 'ok', 'PASS',"
          " 'meta', 'probe', 'json', 'hash', 'ledger', "
          f"'{C['tasks']-2}/{C['tasks']}', 'matrix', 'emit', 'build', 'inject', 'demo.json', 'A0/A1',"
          " 'step++', 'tol', 'source', 'kernel', 'brief[03]', 'fig.2', 'table1', 'date=2026-09', 'v_x', 'omega', 'bounce',"
          " 'value', 'stream', 'collide', 'rate=7.6', 'check', '>>>', 'match', 'diff', 'L2', 'grid64', 'cfg', 'seed=7'];")
routes_js = "const ROUTES = [" + ", ".join(f"'{n}'" for n, c in top) + f", '其他 {other}'];"
code_js = f"""const CODE = [['spec', 'open', '("brief/03")'], ['tasks', 'count', '() // {C['tasks']}'], ['workstreams', 'group', '(tasks) // {C['sectors']}'],
  ['tools', 'probe', '(meta only) // {C['tools']}'], ['data', 'emit', '("demo.json")'], ['html', 'inject', '(data)'],
  ['', 'check_index', '({C['tasks']-2}/{C['tasks']})'], ['', 'register_gaps', '({C['gaps']})'], ['', 'reconcile_proofs', '({C['proof']}/{C['proofTotal']})'],
  ['', 'build_done', '()']];"""
sect_js = "const SECT=['" + "','".join(SHORT[s] for s, _ in secs) + "'];"

# ---------------------------------------------------------------------------
# 配色
# ---------------------------------------------------------------------------
paldata = json.load(io.open(PALJSON, encoding="utf-8"))
G = paldata["全局"]
GLOB = {
    "bg": G["背景"], "text": G["正文"], "dim": G["次级文字"], "faint": G["弱文字"],
    "white": G["白色"], "warn": G["警示琥珀"], "ok": G["成功色"],
    "panel": "#0B0911", "card": "#100D18", "line": "#1A1823", "line2": "#383546",
}
PALETTES = []
for it in paldata["幕配色"]:
    p = dict(GLOB)
    p.update({"i": it["序号"], "use": it["用例"], "en": it["en"],
              "c0": it["c0"], "hi": it["hi"], "fil": it["fil"]})
    PALETTES.append(p)

def tints_js(p):
    def rgb(h):
        h = h.lstrip("#")
        return [int(h[i:i+2], 16) for i in (0, 2, 4)]
    text, hi, c0, fil = rgb(p["text"]), rgb(p["hi"]), rgb(p["c0"]), rgb(p["fil"])
    rows = [text] * 6 + [hi] * 2 + [c0, fil]
    return "const TINTS = [" + ", ".join(f"[{r}, {g}, {b}]" for r, g, b in rows) + "];"

def palette_bar(active):
    cur = next(p for p in PALETTES if p["i"] == active)
    cells = []
    for p in PALETTES:
        on = " on" if p["i"] == active else ""
        cells.append(
            f'<a class="pal{on}" href="collab-{p["i"]:02d}.html" title="{p["i"]:02d} {p["use"]} / {p["en"]}"'
            f' style="--c:{p["c0"]}"><s style="background:{p["c0"]}"></s><b>{p["i"]:02d}</b><em>{p["use"]}</em></a>')
    cells.append('<a class="palAll" href="palettes.html">全部配色 / ALL 12 →</a>')
    return f'''<style id="palStyle">
#pal{{--pal-c0:{cur["c0"]}}}
.ov.pal{{top:10px;right:690px;z-index:6;pointer-events:auto;font:9px/1 "SF Mono",Menlo,monospace;letter-spacing:.08em}}
.ov.pal .palBtn{{display:flex;align-items:center;gap:7px;border:1px solid var(--line2);
  background:rgba(8,7,11,.82);padding:4px 8px;color:var(--dim);cursor:pointer;user-select:none}}
.ov.pal .palBtn:hover{{border-color:var(--dim)}}
.ov.pal .palBtn s{{width:10px;height:10px;display:block;border:1px solid rgba(255,255,255,.22)}}
.ov.pal .palBtn b{{color:var(--text);font-weight:500}}
.ov.pal .palBtn i{{font-style:normal;color:var(--faint)}}
.ov.pal .palPop{{position:absolute;top:30px;right:0;display:none;grid-template-columns:repeat(6,1fr);gap:4px;
  width:318px;padding:8px;background:rgba(7,6,11,.97);border:1px solid var(--line2);
  box-shadow:0 12px 34px rgba(0,0,0,.5)}}
.ov.pal .palPop.open{{display:grid}}
.ov.pal .palPop a{{display:block;text-decoration:none;padding:5px 3px 6px;text-align:center;
  border:1px solid transparent;color:var(--dim)}}
.ov.pal .palPop a:hover{{border-color:var(--line2);background:rgba(255,255,255,.03)}}
.ov.pal .palPop a s{{display:block;height:14px;margin-bottom:5px}}
.ov.pal .palPop a b{{display:block;font:9px/1.2 "SF Mono",Menlo,monospace;color:var(--text);font-weight:500;letter-spacing:.06em}}
.ov.pal .palPop a em{{display:block;font:8px/1.35 "PingFang SC",sans-serif;font-style:normal;color:var(--faint);margin-top:2px;white-space:nowrap}}
.ov.pal .palPop a.on{{border-color:var(--c)}}
.ov.pal .palPop a.on b{{color:var(--c)}}
.ov.pal .palPop a.palAll{{grid-column:1/-1;text-align:right;font:8px/1 "SF Mono",Menlo,monospace;
  color:var(--faint);border:none;border-top:1px solid var(--line);padding:7px 2px 0;margin-top:2px}}
.ov.pal .palPop a.palAll:hover{{background:none;border-color:transparent;color:var(--text)}}
@media (min-aspect-ratio: 21/10){{.ov.pal{{right:350px}}}}
</style>
<div class="ov pal" id="pal">
  <div class="palBtn" id="palBtn" title="切换配色 · {cur["i"]:02d} {cur["use"]}"><s style="background:{cur["c0"]}"></s><b>PAL {cur["i"]:02d}</b><i>▾</i></div>
  <div class="palPop" id="palPop">{"".join(cells)}</div>
</div>
<script>
(function(){{
  var b=document.getElementById('palBtn'), p=document.getElementById('palPop');
  if(!b||!p) return;
  b.addEventListener('click',function(e){{e.stopPropagation();p.classList.toggle('open');}});
  p.addEventListener('click',function(e){{e.stopPropagation();}});
  document.addEventListener('click',function(){{p.classList.remove('open');}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')p.classList.remove('open');}});
}})();
</script>'''

# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def render(pal, out):
    s = io.open(SRC, encoding="utf-8").read()
    palette_notice = """<!--
  COLLAB FIELD / 协作光场
  Copyright (c) 2026 一只黄学长

  Palette reference: ION 离子回路 / agent-display v8.0 theme 08
  Copyright (c) 2026 赛博老爸. https://github.com/cyberdaddyleo/agent-display
  PolyForm Noncommercial 1.0.0.
  Required Notice: Copyright (c) 2026 赛博老爸

  The ledger in this demo is synthetic. See data/demo-network.json.
-->"""
    s = s.replace('-->\n<html lang="en">', '-->\n' + palette_notice + '\n<html lang="zh-CN">', 1)
    pre, rest = s.split("<script>", 1)
    js, post = rest.split("</script>", 1)
    s = colorize(pre, pal) + "<script>" + colorize(js, pal, boost=True) + "</script>" + post

    title = f"AGENT OPS · 协作光场 · {pal['i']:02d} {pal['use']}"
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1)
    s = s.replace('<h1>RYDER CODE / Ms MAIKEBAIs CAT</h1><p>RESEARCH PAPERS → REPRODUCIBLE EXPERIMENTS</p>',
                  f'<h1>AGENT OPS / 协作光场</h1><p>{C["tasks"]} TASKS → {C["sectors"]} WORKSTREAMS → {C["tools"]} TOOLS</p>', 1)

    # KPI
    s = s.replace('<div class="k">PAPERS</div><div class="v" id="k0">64</div>',
                  f'<div class="k">TASKS</div><div class="v" id="k0">{C["tasks"]}</div>', 1)
    s = s.replace('<div class="k">AGENTS</div><div class="v pink" id="k1">12</div>',
                  f'<div class="k">TOOLS</div><div class="v pink" id="k1">{C["tools"]}</div>', 1)
    s = s.replace('<div class="k">METHODS</div><div class="v" id="k2">11</div>',
                  f'<div class="k">WORKSTREAMS</div><div class="v" id="k2">{C["sectors"]}</div>', 1)
    s = s.replace('<div class="k">REF. SCENES</div><div class="v" id="k3">28</div>',
                  f'<div class="k">GAPS</div><div class="v" id="k3">{C["gaps"]}</div>', 1)
    s = s.replace('<div class="k">FURTHER REVIEW</div><div class="v" id="k4">4</div>',
                  f'<div class="k">PROOFS</div><div class="v" id="k4">{C["proof"]}/{C["proofTotal"]}</div>', 1)
    s = s.replace('<div class="big" id="stBig">7 / 11 METHODS · 4 PENDING</div><div class="sm">independent runs · shared event bus</div>',
                  f'<div class="big" id="stBig">{C["tasks"]-2} / {C["tasks"]} MERGED · 2 PENDING</div><div class="sm">single source · spec → json → build</div>', 1)
    s = s.replace('<b id="chkK">STABILITY CHECK</b><span id="chkV">CFL = |u| Δt / Δx</span>',
                  '<b id="chkK">DATA LINEAGE</b><span id="chkV">SPEC → JSON → BUILD</span>', 1)
    s = s.replace("document.getElementById('stBig').textContent = `${m} / 11 METHODS · ${11 - m} PENDING`;",
                  f"document.getElementById('stBig').textContent = '{C['tasks']-2} / {C['tasks']} MERGED · 2 PENDING';", 1)

    # 面板标题 / 说明
    for a, b in [
        ('<h3>INVESTIGATION FEED</h3>', '<h3>任务流 / TASK FEED</h3>'),
        ('<h3>METHOD WORKSPACE</h3>', '<h3>构建管线 / BUILD</h3>'),
        ('<h3>SHARED SCENE / DIFFERENCE FIELD</h3>', '<h3>双视角 / DIFFERENCE FIELD</h3>'),
        ('<h3>SOURCE / EXTRACTION ROUTES</h3>', '<h3>工具 / TOOL ROUTES</h3>'),
        ('<h3>VALIDATION / SAMPLE BUFFER</h3>', '<h3>核验 / SAMPLE BUFFER</h3>'),
        ('<h3>12 AGENTS / DISPATCH</h3>', '<h3>12 工作流 / DISPATCH</h3>'),
        ('<h3>METHOD / REFERENCE INDEX</h3>', '<h3>凭据 / CREDENTIALS</h3>'),
        ('same input · local difference · inspect source', 'same brief · two views · diff the source'),
        ('pages → equations → runnable source', 'brief → spec → build'),
        ('illustrative / source check required', 'illustrative data / verify against source'),
        ('independent jobs / shared event bus', 'independent jobs · shared context'),
        ('28 scenes / 7 matched / 4 further review',
         f'{C["proofTotal"]} proofs / {C["proof"]} matched / {C["proofTotal"]-C["proof"]} open'),
        ('19 项凭据 / 0 已齐 / 19 待补',
         f'{C["proofTotal"]} 项凭据 / {C["proof"]} 已齐 / {C["proofTotal"]-C["proof"]} 待补'),
    ]:
        s = s.replace(a, b, 1)

    # 等待播放时不要整段消失（截图/投影更容易读）
    s = s.replace("@keyframes bl{50%{opacity:0}}", "@keyframes bl{50%{opacity:.35}}", 1)

    # 上游残留的 PAPER 表头
    s = s.replace('<span class="h">PAPER</span>', '<span class="h">TOOL</span>', 1)

    # 画布检查项：换成数据管线语义
    checks = ("const CHECKS = [['SCHEMA CHECK', 'fields = 14 / 14'], ['IDEMPOTENCE', 'build(x) == build(x)'], "
              f"['OPEN GAPS', '{C['gaps']}'], ['LINEAGE', 'spec → json → build'], "
              f"['PROOF', '{C['proof']} / {C['proofTotal']} signed']];")
    s = re.sub(r"const CHECKS = \[[\s\S]*?\];", checks, s, count=1)

    # 配色相关的两组纯数字色串
    c0 = hx2rgb(pal['c0']); hi = hx2rgb(pal['hi'])
    hh, hl, hs = colorsys.rgb_to_hls(*[x / 255 for x in hi])
    h0 = c0 if (hs < 0.15 and hl > 0.90) else hi
    h1 = mix((255, 255, 255), h0, 0.55)
    hz = lambda c: f"'{c[0]},{c[1]},{c[2]}'"
    s = s.replace("const HAZE_COL = ['196,180,252', '242,242,252', '190,222,222'];",
                  f"const HAZE_COL = [{hz(h0)}, {hz(h1)}, {hz(c0)}];", 1)
    s = s.replace("const col = c.tint ? '200,190,250' : '255,255,255';",
                  f"const col = c.tint ? {hz(h0)} : {hz(h1)};", 1)
    s = re.sub(r"const TINTS = \[[\s\S]*?\];", tints_js(pal), s, count=1)

    # 数据数组
    s = re.sub(r"const ACTS = \[[\s\S]*?\];", acts_js, s, count=1)
    s = re.sub(r"const CODE = \[[\s\S]*?\];", code_js, s, count=1)
    s = re.sub(r"const ROUTES = \[.*?\];", routes_js, s, count=1)
    s = re.sub(r"const HEAD = \[[\s\S]*?\];", head_js, s, count=1)
    s = re.sub(r"const KEYS = \[.*?\];", keys_js, s, count=1)
    s = re.sub(r"const CODE_T = \[[\s\S]*?\];", code_t_js, s, count=1)
    s = re.sub(r"const TOK = \[[\s\S]*?\];", tok_js, s, count=1)
    s = s.replace("let feedN = 37;", "let feedN = 96;", 1)
    s = s.replace("const AG = Array.from({ length: 12 }, (_, i) => ({ id: String(i + 1).padStart(2, '0'), role: ROLES[i % 4], p: rnd() * 8, sp: rr(0.6, 2), st: 'working' }));",
                  sect_js + "\nconst AG = Array.from({ length: 12 }, (_, i) => ({ id: String(i + 1).padStart(2, '0'), role: ROLES[i % 4], sector: SECT[i], p: rnd() * 8, sp: rr(0.6, 2), st: 'working' }));", 1)
    s = s.replace('<span class="rl">${a.role}</span>', '<span class="rl">${a.sector}</span>', 1)

    # 侧栏
    tpl = io.open(TPL, encoding="utf-8").read()
    tpl = colorize(tpl, pal, side=True)
    ledger = {
        "tasks": [{"id": t["id"], "date": t["date"], "tool": t["tool"], "sector": SHORT[t["sector"]],
                   "title": q(t["title"], 40), "rows": t.get("rows", 0), "ev": t["ev"]} for t in tasks],
        "sect": {SHORT[a]: b for a, b in secs},
        "tools": C["tools"], "tasksN": C["tasks"], "gaps": C["gaps"],
        "proof": C["proof"], "proofTotal": C["proofTotal"],
        "span": f'{tasks[0]["date"]} → {tasks[-1]["date"]}',
    }
    s = s.replace("</body>", tpl.replace("__LEDGER__", json.dumps(ledger, ensure_ascii=False)) + "</body>", 1)

    # 顶部切换器 + 音频占位
    s = s.replace('<audio id="bgmAudio"', palette_bar(pal["i"]) + '<audio id="bgmAudio"', 1)
    s = s.replace("au.addEventListener('error', () => { txt.textContent = 'BGM 文件未找到'; box.classList.remove('on', 'wait'); });",
                  "au.addEventListener('error', () => { txt.textContent = 'BGM 文件未找到'; box.classList.remove('on', 'wait'); box.style.display = 'none'; });", 1)

    io.open(out, "w", encoding="utf-8").write(s)
    return len(s.encode())

if __name__ == "__main__":
    for p in PALETTES:
        out = os.path.join(BASE, f'collab-{p["i"]:02d}.html')
        n = render(p, out)
        print(f'{p["i"]:02d} {p["use"]:<6} {p["c0"]} {n//1024} KB')
    shutil.copyfile(os.path.join(BASE, "collab-09.html"), os.path.join(BASE, "index.html"))
    print("index.html ← 09 综合总览")
