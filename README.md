# ETF Dividend Monitor

A [CodeBuddy](https://www.codebuddy.ai) skill for automated dividend ETF investment signal monitoring and IMA knowledge base archiving.

## Overview

This skill monitors 4 Chinese dividend ETFs using the MA250 (250-day Moving Average) deviation strategy, generates investment signals, saves results as Markdown files, and automatically archives them to the IMA knowledge base.

## Monitored ETFs

| ETF Name | Code | Index |
|----------|------|-------|
| 红利低波100ETF博时 | 159307 | CSI Dividend Low Volatility 100 |
| 红利低波ETF易方达 | 563020 | CSI Dividend Low Volatility |
| 红利低波50ETF南方 | 515450 | CSI Dividend Low Volatility 50 |
| 红利ETF易方达 | 515180 | CSI Dividend |

## Signal Strategy

The strategy is based on the deviation between current price and MA250:

| Deviation Range | Signal Level | Recommendation |
|----------------|--------------|----------------|
| ≤ -10% | 🔴 Severely Undervalued | Strongly recommended to double DCA |
| -10% ~ -5% | 🟠 Significantly Undervalued | Recommended to increase DCA amount |
| -5% ~ -2% | 🟡 Slightly Undervalued | Recommended normal DCA |
| -2% ~ 0% | 🟢 Below Average | Consider DCA |
| > 0% | 😴 Above Average | Hold and wait |

> DCA = Dollar Cost Averaging (定投)

## Workflow

1. **Monitor** — Execute `check_dividend_etfs.py` to fetch real-time prices and calculate MA250 deviation
2. **Save** — Save the full report as `红利ETF监控_YYYYMMDD.md`
3. **Archive** — Upload the `.md` file to IMA knowledge base via OpenAPI (create_media → COS Upload → add_knowledge)

## Prerequisites

- Python 3 (no external packages required)
- Node.js (for IMA upload scripts)
- IMA credentials configured at `~/.config/ima/` (`client_id` and `api_key`)
- [ima-skill](https://github.com/) installed at `~/.codebuddy/skills/ima-skill/`

## Installation

Place this skill in your CodeBuddy skills directory:

```bash
# User-level (available across all projects)
~/.codebuddy/skills/etf-dividend-monitor/
```

## Usage

Trigger the skill by saying:

- "执行红利ETF监测"
- "检查红利ETF定投信号"
- "红利ETF定投检查"

Or configure it as a CodeBuddy automation for scheduled execution (e.g., weekdays at 09:45).

## Project Structure

```
etf-dividend-monitor/
├── SKILL.md                         # Skill instructions for CodeBuddy
├── README.md                        # This file (English)
├── README_zh.md                     # Chinese README
└── scripts/
    └── check_dividend_etfs.py       # Main monitoring script
```

## Data Source

Real-time quotes and historical K-line data are fetched from Tencent Finance API (`qt.gtimg.cn` / `web.ifzq.gtimg.cn`).

## Authors

- **Hank Yang** ([@hankyang](https://github.com/hankyang))
- **Claude** (Anthropic) — AI pair programming assistant

## License

MIT
