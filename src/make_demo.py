#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成公开版虚构数据：data/demo-network.json。

所有任务、日期、工具名、板块名均为合成内容，用于演示数据驱动的协作光场，
不对应任何真实个人、组织或项目。固定随机种子，可重复生成。
"""
import json, os, random
from datetime import date, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data", "demo-network.json")
rng = random.Random(20261028)

# 12 个工作流：全名 / 短名 / 任务数 / 任务标题池
SECTORS = [
    ("研究与洞察", "研究", 13, [
        "整理用户访谈逐字稿", "拆分竞品功能矩阵", "汇总问卷开放题编码",
        "校准研究问题与假设", "访谈录音转写与校对", "绘制用户旅程关键节点",
        "归纳可用性测试观察", "整理桌面研究的 12 条结论", "复核样本配额与招募条件",
        "建立研究证据索引", "对比三套信息架构", "输出研究摘要", "标注异常样本并说明原因",
    ]),
    ("品牌与叙事", "品牌", 11, [
        "收敛品牌语气词表", "校对品牌手册", "整理命名候选与禁用词",
        "重写首页价值主张", "比对两版视觉规范", "梳理品牌触点清单",
        "生成社媒简介短版", "统一中英文标点规范", "校正色彩使用场景",
        "归档品牌资产包", "撰写发布口径 Q&A",
    ]),
    ("界面与交互", "界面", 13, [
        "重做登录流程线框", "梳理空状态与异常态", "校对表单错误提示",
        "整理组件命名与变体", "绘制移动端导航结构", "检查焦点顺序与可达性",
        "统一间距与字号阶梯", "整理图标使用清单", "输出界面走查记录",
        "修正深色模式对比度", "归纳弹窗优先级规则", "建立页面状态矩阵", "复核响应式断点",
    ]),
    ("原型与实现", "原型", 11, [
        "搭建可点击原型", "接入模拟数据与状态", "录制交互演示片段",
        "实现拖拽排序原型", "校准动效时长与缓动", "整理原型交付说明",
        "修复原型路由回退", "生成多语言占位文案", "压测长列表滚动",
        "拆分手势与快捷键", "整理原型验收清单",
    ]),
    ("内容与传播", "内容", 11, [
        "撰写产品更新日志", "整理专题页文案结构", "校对长图文标点",
        "生成短视频分镜草案", "归档素材授权记录", "重写 onboarding 文案",
        "统一术语与缩写", "整理 FAQ 与边界条件", "输出内容日历",
        "校对多语言版本", "撰写空状态提示语",
    ]),
    ("数据与度量", "数据", 10, [
        "合并周报指标口径", "复核漏斗转化计算", "整理事件埋点清单",
        "校对看板筛选逻辑", "生成月度趋势摘要", "清洗重复记录",
        "对比两版指标定义", "输出异常波动说明", "建立指标字典", "核对样本量与置信区间",
    ]),
    ("交付与归档", "交付", 10, [
        "打包版本交付物", "生成变更摘要", "核对交付清单与签收",
        "整理会议决议与待办", "归档评审记录", "更新项目时间线",
        "校对发布说明", "整理风险与依赖清单", "输出交接文档", "清理过期草稿",
    ]),
    ("质量与合规", "合规", 10, [
        "跑通核心路径回归", "复核无障碍检查项", "整理缺陷优先级",
        "校对隐私与授权声明", "检查外链与失效资源", "复核多端渲染差异",
        "整理验收标准", "编写回归用例", "抽查文案与截图一致性", "复核版本号与构建标识",
    ]),
    ("工具与自动化", "工具", 13, [
        "排查本地构建缓存", "整理代理与网络配置", "校准自动化脚本参数",
        "修复批处理路径转义", "比较两版运行时日志", "整理依赖升级影响",
        "建立本地预览命令", "排查字体加载失败", "统一脚本输出格式",
        "整理凭证存放规范", "修复时区导致的日期偏移", "清理临时文件与端口", "记录一次未解释的退出",
    ]),
    ("团队与协作", "协作", 9, [
        "整理周会同步要点", "拆分跨角色任务", "对齐评审口径",
        "更新协作约定", "整理阻塞项与责任人", "复盘一次返工",
        "建立共享术语表", "梳理交接边界", "整理异步沟通模板",
    ]),
    ("教育与培训", "教育", 9, [
        "编写新人上手路径", "整理工具演示脚本", "录制 10 分钟导览",
        "拆解示例任务", "编写常见问题清单", "校对培训材料",
        "设计练习与验收点", "整理反馈与改进项", "更新课程索引",
    ]),
    ("知识资产", "知识", 8, [
        "建立项目索引页", "整理决策记录", "归档复盘笔记",
        "校对知识库链接", "合并重复条目", "补充术语出处",
        "整理模板与片段", "标注待验证结论",
    ]),
]

# 24 个虚构工具代号；数字之和 = 128 条任务
TOOL_COUNTS = {
    "ATLAS": 14, "BEACON": 13, "CIRRUS": 12, "DELTA": 11, "EMBER": 10,
    "FATHOM": 9, "GLYPH": 8, "HELIX": 7, "INDIGO": 6, "JUNO": 6,
    "KITE": 5, "LUMEN": 4, "MOSS": 3, "NOVA": 3, "ORBIT": 3,
    "PULSE": 2, "QUARTZ": 2, "RIFT": 2, "SOL": 2, "TIDE": 2,
    "UMBRA": 1, "VALE": 1, "WISP": 1, "XENON": 1,
}

TOTAL = sum(n for _, _, n, _ in SECTORS)
assert TOTAL == 128, TOTAL
assert sum(TOOL_COUNTS.values()) == 128

# 板块与工具各装一袋，洗牌后配对，保证计数精确且顺序随机
sector_bag = []
for name, short, n, titles in SECTORS:
    sector_bag += [name] * n
tool_bag = []
for name, n in TOOL_COUNTS.items():
    tool_bag += [name] * n
rng.shuffle(sector_bag)
rng.shuffle(tool_bag)

short_of = {name: short for name, short, _, _ in SECTORS}
titles_of = {name: titles for name, _, _, titles in SECTORS}
used = {}

start = date(2026, 1, 5)
span = 264  # 2026-01-05 → 2026-09-26
tasks = []
for i in range(TOTAL):
    sector = sector_bag[i]
    tool = tool_bag[i]
    pool = titles_of[sector]
    k = used.get(sector, 0)
    used[sector] = k + 1
    title = pool[k % len(pool)]
    if k >= len(pool):
        title += f" · {k // len(pool) + 1:02d}"
    day = min(span, round(i * span / (TOTAL - 1)) + rng.choice([0, 0, 0, 1]))
    ev = "session" if i % 4 == 0 else "ledger"
    rows = rng.randint(60, 2400) if ev == "session" else 0
    tasks.append({
        "id": 0,
        "date": (start + timedelta(days=day)).isoformat(),
        "tool": tool,
        "sector": sector,
        "title": title,
        "req": title,
        "deliv": rng.choice(["run-notes.md", "review.html", "spec-v1.2.md", "index.html",
                             "summary.md", "diff-report.html", "handoff.md", "demo.json"]),
        "ev": ev,
        "rows": rows,
    })

tasks.sort(key=lambda t: (t["date"], t["tool"]))
for i, t in enumerate(tasks, 1):
    t["id"] = i

sector_count = {name: sum(1 for t in tasks if t["sector"] == name) for name, _, _, _ in SECTORS}
data = {
    "meta": {
        "title": "COLLAB FIELD · synthetic demo ledger",
        "author": "一只黄学长",
        "note": "全部为合成数据，不含任何真实个人、组织、项目或联系方式。",
        "seed": 20261028,
        "span": f"{tasks[0]['date']} → {tasks[-1]['date']}",
    },
    "tools": [{"name": n, "kind": "agent"} for n in TOOL_COUNTS],
    "counters": {
        "tools": 24, "tasks": TOTAL, "sectors": 12,
        "gaps": 9, "proof": 6, "proofTotal": 24,
    },
    "sectorCount": sector_count,
    "secShort": short_of,
    "tasks": tasks,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print(json.dumps({
    "out": os.path.relpath(OUT, BASE),
    "tasks": len(tasks),
    "tools": len(TOOL_COUNTS),
    "sectors": len(SECTORS),
    "span": data["meta"]["span"],
    "sectorCount": sector_count,
}, ensure_ascii=False, indent=1))
