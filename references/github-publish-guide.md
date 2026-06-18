# GitHub 发布指南

将 CodeBuddy Skill 项目上传到 GitHub 的标准操作流程，供 AI 参考执行。

## 前置条件

- macOS 系统，git 凭证存储在 Keychain 中
- GitHub 用户名：`hankchn`
- GitHub noreply 邮箱：`hankchn@users.noreply.github.com`
- 通过 HTTPS 方式推送（非 SSH）

## 操作流程

### 1. 准备 README 文件

创建中英文双语 README：

- `README.md` — **中文**（默认展示）
- `README_en.md` — 英文

#### 语言切换按钮（居中）

中文 README 顶部：
```html
<p align="center"><b>简体中文</b> | <a href="./README_en.md">English</a></p>
```

英文 README 顶部：
```html
<p align="center"><a href="./README.md">简体中文</a> | <b>English</b></p>
```

#### Contributors 表格

在两个 README 底部都加上：

```html
## Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/hankchn">
        <img src="https://github.com/hankchn.png" width="64" height="64" style="border-radius:50%;" alt="hankchn"/>
        <br />
        <sub><b>hankchn</b></sub>
      </a>
      <br />
      <sub>Hank Yang</sub>
    </td>
    <td align="center">
      <a href="https://claude.ai">
        <img src="https://avatars.githubusercontent.com/u/76263028?s=200" width="64" height="64" style="border-radius:50%;" alt="Claude"/>
        <br />
        <sub><b>Claude</b></sub>
      </a>
      <br />
      <sub>Anthropic AI</sub>
    </td>
  </tr>
</table>
```

> 注：Anthropic 的 GitHub 组织头像 ID 为 `76263028`。

### 2. 准备辅助文件

- `LICENSE` — MIT 许可证，Copyright 写 `Hank Yang & Claude (Anthropic)`
- `.gitignore` — 至少包含 `__pycache__/`、`*.pyc`、`.DS_Store`、`*.zip`

### 3. 初始化 Git 仓库

```bash
cd <项目目录>
git init
git add -A
git commit -m "feat: initial release of <项目名>"
```

### 4. 创建 GitHub 远程仓库

通过 GitHub API 创建（token 从 macOS Keychain 获取）：

```bash
TOKEN=$(security find-internet-password -s github.com -w 2>/dev/null)
curl -s -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<仓库名>",
    "description": "<仓库描述>",
    "private": false,
    "has_issues": true,
    "has_wiki": false
  }' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('html_url','') or d.get('message',''))"
```

### 5. 推送代码

```bash
git remote add origin https://github.com/hankchn/<仓库名>.git
git push -u origin main
```

### 6. 修正 Contributors 显示

GitHub 右侧的 Contributors 面板通过 commit 的 author 信息自动生成。要让 `hankchn` 和 `Claude` 都显示：

**关键规则**：
- commit author 必须使用 GitHub noreply 邮箱：`hankchn <hankchn@users.noreply.github.com>`
- 每个 commit message 末尾加上 `Co-authored-by: Claude <noreply@anthropic.com>`

**方法 A — 新仓库直接用正确格式提交**：

```bash
git commit -m "feat: initial release

Co-authored-by: Claude <noreply@anthropic.com>" \
  --author="hankchn <hankchn@users.noreply.github.com>"
```

**方法 B — 已有仓库批量修正历史**：

```bash
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f \
  --msg-filter 'cat && echo "" && echo "Co-authored-by: Claude <noreply@anthropic.com>"' \
  --env-filter '
    export GIT_AUTHOR_NAME="hankchn"
    export GIT_AUTHOR_EMAIL="hankchn@users.noreply.github.com"
    export GIT_COMMITTER_NAME="hankchn"
    export GIT_COMMITTER_EMAIL="hankchn@users.noreply.github.com"
  ' -- --all

git push --force origin main
```

> ⚠️ `filter-branch` 会重写历史，仅在个人仓库或首次发布时使用。

### 7. 验证

推送后访问 `https://github.com/hankchn/<仓库名>` 确认：

- [x] README 默认展示中文
- [x] 语言切换按钮居中显示
- [x] 右侧 Contributors 显示 hankchn 和 Claude（可能需要几分钟缓存刷新）
- [x] LICENSE 显示为 MIT license

## 注意事项

- GitHub 识别 contributor 依赖于邮箱关联，必须使用 `hankchn@users.noreply.github.com`
- `Co-authored-by` trailer 必须在 commit message body 中（空行之后），格式严格为 `Co-authored-by: Name <email>`
- GitHub token 存储在 macOS Keychain（`security find-internet-password -s github.com -w`），无需手动管理
- 敏感信息（token、API key 等）绝不能出现在代码中，仅使用占位符如 `<cos_credential.token>`
