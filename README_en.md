<p align="center"><a href="./README.md">简体中文</a> | <b>English</b></p>

# etf-dividend-monitor

One-line summary: this Skill monitors the MA250 deviation of four Chinese dividend ETFs, generates dollar-cost-averaging observation signals, and saves the result as an archivable Markdown report.

## What this version can do

- Fetch current prices and historical K-line data for four dividend ETFs.
- Calculate the MA250 moving average and current-price deviation.
- Output observation levels such as severe undervaluation, clear undervaluation, mild undervaluation, slightly below average, or above average.
- Generate a Markdown report named `红利ETF监控_YYYYMMDD.md`.
- Optionally archive the daily report to a user-specified IMA knowledge base and folder through IMA OpenAPI.

## Who it is for

- Individual investors who want a regular signal for whether dividend ETFs are below a long-term moving average.
- Users who want to keep daily monitoring records in a knowledge base for later review.
- Users who already have IMA credentials and want to automate monitoring, saving, and archiving.

## Usage example

Run the monitor:

```bash
python3 scripts/check_dividend_etfs.py
```

Example output includes:

```text
Dividend ETF monitor
- ETF name
- Current price
- MA250
- Deviation
- Observation signal
```

If archiving is configured, the report is saved as Markdown and uploaded to the user's selected IMA knowledge base.

## Quick start

Install as a Codex Skill:

```bash
git clone https://github.com/hankchn/etf-dividend-monitor.git
mkdir -p ~/.codex/skills/etf-dividend-monitor
cp -R etf-dividend-monitor/{SKILL.md,scripts} ~/.codex/skills/etf-dividend-monitor/
```

Run manually:

```bash
cd ~/.codex/skills/etf-dividend-monitor
python3 scripts/check_dividend_etfs.py
```

Trigger through an agent:

```text
Run the dividend ETF monitor.
```

## Common uses

- Run on weekday mornings to create a daily observation report.
- Read the script output as a research signal before doing further analysis.
- Configure IMA credentials and archive Markdown reports to a selected knowledge base.
- Use the report as a personal observation log, not as an automatic trading instruction.

## Current limitations

- Data comes from Tencent Finance endpoints; endpoint outages or field changes may break the script.
- On non-trading days, data usually reflects the previous trading day.
- MA250 deviation is an observation signal, not investment advice.
- IMA upload requires local credentials and should resolve the target by knowledge-base and folder name at runtime.

## Security and privacy

- Do not commit IMA `client_id`, `api_key`, knowledge-base IDs, folder IDs, or upload credentials.
- This repository should not hardcode personal knowledge-base identifiers; archive targets should come from user configuration or runtime lookup.
- Monitoring output is for personal research and review only, and is not investment advice.

## Technical notes

- `scripts/check_dividend_etfs.py` fetches market data, calculates MA250, and prints the monitoring result.
- `SKILL.md` describes the agent workflow, report naming, and IMA archiving process.
- Markdown reports can be used in a knowledge base, note system, or versioned review workflow.

## Roadmap

- Add configurable ETF lists.
- Add retry and fallback data-source behavior.
- Add historical signal backtesting and hit-rate review.

## License

[MIT](./LICENSE)

## Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/hankchn">
        <img src="https://github.com/hankchn.png" width="64" height="64" style="border-radius:50%;" alt="hankchn" />
        <br />
        <sub><b>hankchn</b></sub>
      </a>
      <br />
      <sub>Hank Yang</sub>
    </td>
    <td align="center">
      <a href="https://openai.com/codex">
        <img src="https://github.com/openai.png" width="64" height="64" style="border-radius:50%;" alt="Codex" />
        <br />
        <sub><b>Codex</b></sub>
      </a>
      <br />
      <sub>OpenAI Codex</sub>
    </td>
  </tr>
</table>
