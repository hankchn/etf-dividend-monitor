# 红利ETF定投监测

一个 [CodeBuddy](https://www.codebuddy.ai) Skill，用于自动化红利ETF定投信号监测与IMA知识库归档。

## 概述

此 Skill 监控 4 只中国红利ETF，使用 MA250（250日均线）偏离度策略生成定投信号，将监测结果保存为 Markdown 文件，并自动上传到 IMA 知识库归档。

## 监控标的

| ETF名称 | 代码 | 跟踪指数 |
|---------|------|----------|
| 红利低波100ETF博时 | 159307 | 中证红利低波动100 |
| 红利低波ETF易方达 | 563020 | 中证红利低波动 |
| 红利低波50ETF南方 | 515450 | 中证红利低波动50 |
| 红利ETF易方达 | 515180 | 中证红利 |

## 信号策略

基于当前价格与 MA250 均线的偏离度判断：

| 偏离度范围 | 信号等级 | 建议 |
|-----------|---------|------|
| ≤ -10% | 🔴 严重低估 | 强烈建议加倍定投 |
| -10% ~ -5% | 🟠 明显低估 | 建议增加定投金额 |
| -5% ~ -2% | 🟡 轻度低估 | 建议正常定投 |
| -2% ~ 0% | 🟢 略低于均线 | 可考虑定投 |
| > 0% | 😴 高于均线 | 持有观望 |

## 工作流程

1. **监测** — 执行 `check_dividend_etfs.py` 获取实时价格，计算 MA250 偏离度
2. **保存** — 将完整报告保存为 `红利ETF监控_YYYYMMDD.md`
3. **归档** — 通过 IMA OpenAPI 上传 `.md` 文件到知识库（create_media → COS 上传 → add_knowledge）

## 前置条件

- Python 3（无需额外安装包）
- Node.js（用于 IMA 上传脚本）
- IMA 凭证已配置在 `~/.config/ima/`（`client_id` 和 `api_key`）
- [ima-skill](https://github.com/) 已安装在 `~/.codebuddy/skills/ima-skill/`

## 安装

将此 Skill 放置在 CodeBuddy skills 目录中：

```bash
# 用户级（所有项目可用）
~/.codebuddy/skills/etf-dividend-monitor/
```

## 使用方式

通过以下方式触发：

- "执行红利ETF监测"
- "检查红利ETF定投信号"
- "红利ETF定投检查"

也可配置为 CodeBuddy 自动化任务，实现定时执行（如工作日 09:45）。

## 项目结构

```
etf-dividend-monitor/
├── SKILL.md                         # Skill 指令文档（CodeBuddy 读取）
├── README.md                        # 英文说明
├── README_zh.md                     # 中文说明（本文件）
└── scripts/
    └── check_dividend_etfs.py       # 主监测脚本
```

## 数据来源

实时行情和历史K线数据来自腾讯财经接口（`qt.gtimg.cn` / `web.ifzq.gtimg.cn`）。

## 作者

- **Hank Yang** ([@hankchn](https://github.com/hankchn))
- **Claude** (Anthropic) — AI 结对编程助手

## 许可证

MIT
