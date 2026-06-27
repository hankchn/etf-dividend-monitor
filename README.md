<p align="center"><b>简体中文</b> | <a href="./README_en.md">English</a></p>

# etf-dividend-monitor

一句话说明：这个 Skill 帮你监控 4 只中国红利 ETF 的 MA250 偏离度，生成定投观察信号，并把结果保存为可归档的 Markdown 报告。

## 这个版本能做什么

- 获取 4 只红利 ETF 的实时价格和历史 K 线数据。
- 计算 MA250 均线和当前价格偏离度。
- 按偏离区间输出“严重低估、明显低估、轻度低估、略低于均线、高于均线”等观察信号。
- 生成 `红利ETF监控_YYYYMMDD.md` 格式的 Markdown 报告。
- 可结合 IMA OpenAPI，把每日报告归档到用户指定知识库和文件夹。

## 适合谁

- 需要定期观察红利 ETF 是否进入定投区间的个人投资者。
- 想把每日监控结果沉淀到知识库里，方便回看和复盘的人。
- 已经有 IMA 凭证，并希望把监控、保存、归档串成自动化流程的人。

## 使用示例

运行监控脚本：

```bash
python3 scripts/check_dividend_etfs.py
```

示例输出会包含：

```text
红利ETF监控
- ETF 名称
- 当前价格
- MA250
- 偏离度
- 观察信号
```

如果配置了归档流程，报告会保存为 Markdown 文件，再上传到用户指定的 IMA 知识库。

## 快速开始

安装为 Codex Skill：

```bash
git clone https://github.com/hankchn/etf-dividend-monitor.git
mkdir -p ~/.codex/skills/etf-dividend-monitor
cp -R etf-dividend-monitor/{SKILL.md,scripts} ~/.codex/skills/etf-dividend-monitor/
```

手动运行：

```bash
cd ~/.codex/skills/etf-dividend-monitor
python3 scripts/check_dividend_etfs.py
```

在 Agent 中触发：

```text
执行红利ETF监测
```

## 常见用法

- 工作日上午固定时间运行，生成当天观察报告。
- 只查看脚本输出，用于人工判断是否需要继续研究。
- 配置 IMA 凭证后，把 Markdown 报告归档到指定知识库。
- 将报告作为每日投资观察记录，不直接作为买卖指令。

## 当前限制

- 数据来自腾讯财经接口，接口不可用或字段变化时脚本可能失败。
- 非交易日拿到的通常是上一交易日数据。
- MA250 偏离度只是观察信号，不等于投资建议。
- IMA 上传需要用户在本机配置凭证，并通过知识库名称和文件夹名称定位目标位置。

## 安全与隐私说明

- 不要把 IMA `client_id`、`api_key`、知识库 ID、folder ID 或上传凭证提交到仓库。
- 本仓库不应写死个人知识库标识；归档目标应由用户配置或运行时查找。
- 监控结果仅供个人研究和复盘，不构成投资建议。

## 技术实现

- `scripts/check_dividend_etfs.py` 获取行情、计算 MA250 并输出监控结果。
- `SKILL.md` 描述 Agent 工作流、报告命名和 IMA 归档步骤。
- Markdown 报告可供知识库、笔记系统或版本化复盘使用。

## Roadmap

- 增加更多 ETF 配置方式。
- 增加失败重试和数据源降级。
- 增加历史信号回测和命中率评估。

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
