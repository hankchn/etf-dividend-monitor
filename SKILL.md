---
name: etf-dividend-monitor
description: |
  红利ETF定投监测与IMA知识库归档 skill。执行批量ETF定投信号检测（基于MA250偏离度策略），
  将监测结果保存为Markdown文件，并自动上传到IMA知识库归档。
  当用户要求执行红利ETF监测、定投检查、ETF定投信号监控，或提到"红利ETF"+"监测/检查/定投"时触发此skill。
---

# 红利ETF定投监测 + IMA归档

## 概述

此 skill 执行红利ETF批量定投信号监测（基于MA250均线偏离度策略），将结果保存为 `.md` 文件并上传到 IMA 知识库归档。

## 触发条件

- 用户要求执行红利ETF监测/定投检查
- 自动化任务调度执行（工作日 09:45）
- 用户提到 "红利ETF" + "监测/检查/定投/信号"

## 工作流

### Step 1: 执行监测脚本

```bash
cd "<SKILL_DIR>/scripts" && python3 check_dividend_etfs.py
```

脚本功能：
- 监控 4 只红利ETF：159307、563020、515450、515180
- 通过腾讯财经接口获取实时价格和 350 个交易日历史数据
- 计算 MA250 均线及偏离度
- 当价格低于 MA250 时输出定投信号

`<SKILL_DIR>` 为本 skill 的目录路径。

### Step 2: 保存监测结果

将脚本的完整输出保存为 Markdown 文件：

- **文件名格式**: `红利ETF监控_YYYYMMDD.md`
- **保存路径**: 工作目录（由 automation 的 `cwds` 或用户指定）
- **内容**: 脚本的完整标准输出（含表情符号和格式）

### Step 3: 上传到 IMA 知识库

使用 IMA OpenAPI 将 .md 文件上传到指定知识库文件夹。

#### 归档目标

默认按用户指定的知识库名称和文件夹名称执行。不要在仓库中写死个人 `knowledge_base_id`、`folder_id`、`media_id` 或上传凭证。

执行上传前应先按名称查询可用知识库和文件夹；如果名称不完全匹配，列出候选项并向用户确认最近的真实目标，不能猜测 ID。

#### 上传流程

IMA 凭证存储在 `~/.config/ima/`（`client_id` 和 `api_key` 文件）。

```bash
# 加载凭证
IMA_CLIENT_ID="$(cat ~/.config/ima/client_id 2>/dev/null)"
IMA_API_KEY="$(cat ~/.config/ima/api_key 2>/dev/null)"
```

如凭证缺失，终止操作并提示用户配置。

**上传三步流程**：

1. **前置检查** — 使用 preflight-check 脚本验证文件类型和大小：

```bash
node <IMA_SKILL_DIR>/knowledge-base/scripts/preflight-check.cjs --file "<md_file_path>"
```

`<IMA_SKILL_DIR>` 为 `~/.codebuddy/skills/ima-skill` 的实际路径。

2. **create_media** — 获取 COS 上传凭证：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/create_media" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "<文件名>",
    "file_size": <字节数>,
    "content_type": "text/markdown",
    "knowledge_base_id": "<resolved_knowledge_base_id>",
    "file_ext": "md"
  }'
```

从返回值提取 `media_id` 和 `cos_credential` 各字段。

3. **COS Upload** — 上传文件到腾讯云 COS：

```bash
node <IMA_SKILL_DIR>/knowledge-base/scripts/cos-upload.cjs \
  --file "<md_file_path>" \
  --secret-id "<cos_credential.secret_id>" \
  --secret-key "<cos_credential.secret_key>" \
  --token "<cos_credential.token>" \
  --bucket "<cos_credential.bucket_name>" \
  --region "<cos_credential.region>" \
  --cos-key "<cos_credential.cos_key>" \
  --content-type "text/markdown" \
  --start-time "<cos_credential.start_time>" \
  --expired-time "<cos_credential.expired_time>"
```

4. **add_knowledge** — 将文件关联到知识库：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/add_knowledge" \
  -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
  -H "ima-openapi-apikey: $IMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "media_type": 7,
    "media_id": "<media_id>",
    "title": "<文件名>",
    "knowledge_base_id": "<resolved_knowledge_base_id>",
    "folder_id": "<resolved_folder_id>",
    "file_info": {
      "cos_key": "<cos_credential.cos_key>",
      "file_size": <字节数>,
      "file_name": "<文件名>"
    }
  }'
```

`retcode=0` 表示成功。

### Step 4: 输出结果摘要

完成后输出简洁摘要：

```
📊 红利ETF定投监测 (YYYY-MM-DD)
- X 只触发定投信号 / 全部观望
- 各ETF: 名称 当前价 MA250 偏离度 信号
- 文件已保存: 红利ETF监控_YYYYMMDD.md
- IMA归档: ✅ / ❌
```

## 监测策略说明

| 偏离度范围 | 信号等级 | 建议 |
|-----------|---------|------|
| ≤ -10% | 🔴 严重低估 | 强烈建议加倍定投 |
| -10% ~ -5% | 🟠 明显低估 | 建议增加定投金额 |
| -5% ~ -2% | 🟡 轻度低估 | 建议正常定投 |
| -2% ~ 0% | 🟢 略低于均线 | 可考虑定投 |
| > 0% | 😴 高于均线 | 持有观望 |

## 依赖

- Python 3（系统自带即可，无需额外包）
- Node.js（用于 IMA 上传脚本）
- IMA 凭证已配置（`~/.config/ima/client_id` 和 `api_key`）
- ima-skill 已安装（`~/.codebuddy/skills/ima-skill/`）

## 注意事项

- 仅在交易日（周一至周五）执行有意义，非交易日获取的是上一交易日数据
- 脚本请求间有 0.5 秒间隔避免限流
- IMA 上传时 `title` 必须等于 `file_name`（含扩展名）
- 文件为 Markdown 格式，media_type=7，content_type=text/markdown
