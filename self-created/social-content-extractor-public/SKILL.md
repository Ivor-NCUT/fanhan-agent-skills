---
name: social-content-extractor-public
description: Extract titles, metrics, links, and copy from public Xiaohongshu, Douyin, WeChat Official Account, and webpage URLs through AI Conductor. Use for a post/article URL or an account/profile URL; when no API key is configured, guide the user through AI Conductor registration before extraction.
---

# 社媒内容提取（对外版）

把用户给出的公开链接交给 `{baseDir}/scripts/extract_social_content.py`，返回统一作品清单。单篇输出标题、链接、作者、发布时间、作品数据和文案；主页输出每条已获取作品的同样字段。

## 首次使用

先直接运行提取命令。若脚本提示尚未配置 API key：

1. 请用户打开 [AI Conductor 开发者平台](https://dev.aiconductor.fun/) 注册账号并创建 API key。
2. 请用户把 API key 发给 Agent。不要要求用户把 key 写进 Skill 文件或压缩包。
3. 收到 key 后，以交互终端运行下面的配置命令，通过 stdin 输入 key；不得把 key 放进命令参数、回复、日志或长期记忆：

   ```bash
   python3 "{baseDir}/scripts/extract_social_content.py" --configure
   ```

4. 配置成功后继续原提取任务，不要求用户重新发送链接。脚本把 key 保存到当前用户的 `~/.config/aiconductor/api_key`，文件权限为 `600`；`AICONDUCTOR_API_KEY` 可临时覆盖该配置。

## 提取

```bash
python3 "{baseDir}/scripts/extract_social_content.py" '<链接或分享文本>'
python3 "{baseDir}/scripts/extract_social_content.py" '<主页链接>' --kind profile --max-pages 3
python3 "{baseDir}/scripts/extract_social_content.py" '<主页链接>' --kind profile --max-pages 3 --output result.md
```

## 执行边界

- 自动识别小红书、抖音、公众号和普通网页；短链无法判定作品/主页时显式加 `--kind item|profile`。
- 主页接口按页计费。用户未给页数时先用 1 页预览；公众号可依据返回的总页数估算后续范围，抖音/小红书无法证明总量时先询问页数上限。
- 用户只要列表、不需要公众号全文时加 `--no-copy`，避免逐篇调用正文接口。
- 只有 `complete: true` 才称为“全量”；`null` 或 `false` 必须同时报告 `complete_note`、实际页数和作品数。
- 不抓取私密、登录后或已删除内容；单条失败保留 `copy_error`，不丢弃其他成功作品。
- API key 只来自用户本机配置或环境变量。禁止把 key 写入 Skill、压缩包、输出、群消息、日志、长期记忆或公开仓库。

需要核对接口、计费或字段映射时读取 [API 契约](references/api-contract.md)。

## 完成标准

输出包含 `platform`、`kind`、`count`、`complete`、`complete_note` 和 `items`；每条 item 至少有 `title`、`url`、`copy`、`metrics`。接口错误必须脱敏并明确失败，不能用空结果冒充成功。
