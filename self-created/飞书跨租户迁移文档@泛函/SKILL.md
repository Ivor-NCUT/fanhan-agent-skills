---
name: feishu-cross-tenant-migration-fanhan
description: Use this skill whenever the user wants to migrate, copy, consolidate, archive, rescue, or rebuild Feishu/Lark cloud documents, Wiki pages, Drive folders, Sheets, Slides, Base/Bitable apps, or ordinary files from one tenant/account into another tenant. This skill is especially important for cross-tenant Feishu moves using lark-cli, first-time lark-cli installation, multi-account Feishu authorization, Markdown-first document migration, QR/user authorization, migration manifests, and non-technical onboarding. Use it even if the user only says “把这个租户的文档搬到另一个飞书”, “跨租户迁移”, “创建副本”, “文档搬家”, or “飞书资料归档”.
---

# 飞书跨租户迁移文档@泛函

This skill turns a Feishu/Lark document migration into a guided, auditable workflow. The user may be non-technical, but they usually know how to open Feishu, scan a QR code, copy a folder link, and check whether a migrated document looks right. Keep the interface simple for them; handle the technical inventory, command choices, retries, and manifests yourself.

Use `lark-cli` for Feishu work. Do not switch to manual browser operations, raw OpenAPI scripts, or another Feishu connector unless the user explicitly asks.

## What Good Looks Like

Finish with:

- A target Feishu folder in the destination tenant, with one subfolder per source tenant/account unless the user asks for a different layout.
- A durable local migration workspace containing raw logs, downloaded/exported files if any, a manifest, a summary, and a failure list.
- A short user-facing report with counts by source, migration method, status, and important limitations.
- No source documents deleted or moved.

Prefer a migration that preserves readable content and reviewability over a fast black-box copy that hides failures.

## Onboarding A Non-Technical User

Guide the user in small steps. Do not ask them for implementation details; ask for Feishu facts they can provide.

Start by clarifying these four things:

1. Source tenants/accounts: which Feishu tenants should be migrated?
2. Destination tenant/account: which tenant should hold the final copy?
3. Target location: should you create a new root folder, or use an existing folder link?
4. Scope: migrate only “my documents”, a named folder/wiki, or everything searchable from those source accounts?

Use this phrasing when helpful:

```text
我需要你确认三件事：
1. 哪些旧租户要搬？
2. 最终搬到哪个新租户？
3. 新租户里放在哪个文件夹？如果没有，我可以新建一个总文件夹。

之后我会逐个账号发授权二维码。你只需要用对应租户的飞书账号扫码确认。
```

Before large batches, run a small proof-of-concept migration of 3-10 mixed files. Ask the user to spot-check a few target links before migrating hundreds of items.

## First-Time Setup

Assume the user may not have `lark-cli` installed or authorized. Check this before discussing migration mechanics.

### Check And Install lark-cli

Run:

```bash
command -v lark-cli
lark-cli --version
```

If `lark-cli` is missing, install it with npm:

```bash
npm install -g @larksuite/cli
lark-cli --version
```

If npm or Node.js is missing, stop and explain the smallest next step in plain language. For macOS users, suggest installing Node.js with Homebrew if Homebrew is available:

```bash
brew install node
npm install -g @larksuite/cli
```

If `lark-cli` exists, update it before a migration unless the user asks not to:

```bash
lark-cli update
```

Tell the user that this updates both the CLI and bundled Feishu skills.

### Initial App/Profile Setup

List profiles:

```bash
lark-cli profile list
```

If there are no usable profiles, initialize configuration:

```bash
lark-cli config init --new
```

If the user already has Feishu app credentials for each tenant, create explicit profiles instead of overloading one default profile:

```bash
lark-cli profile add --name <tenant-slug> --brand feishu --app-id <app-id> --app-secret-stdin
```

Use human-readable profile names such as:

```text
source-bibai
source-feixingjia
source-personal
target-aimanziyi
```

Do not ask a non-technical user to invent profile names. Propose names from their tenant names and confirm.

## Safety Rules

- Do not rely on “把链接发给目标账号再手动创建副本” as the main method. It is useful for one-off rescue, but too slow and hard to audit for large migrations.
- Do not use `drive +pull` / `drive +push` as the main migration path. They are useful for ordinary files, but they skip or cannot faithfully handle many online document types.
- Do not silently use Docx export for modern Docx documents when Markdown export is available. Markdown-first usually keeps structure cleaner for online docs.
- Do not delete, move, or rename source documents during migration.
- Do not treat every `permission denied` as a transient failure. First distinguish missing OAuth scopes, target folder permissions, source document permissions, and unsupported cross-tenant copy behavior.
- Do not count search duplicates as multiple migrated documents. Deduplicate before final reporting.

## Profiles And Authorization

Use source profiles for search/export/download and the target profile for create/import/upload/copy.

Check profiles first:

```bash
lark-cli profile list
lark-cli auth status --profile <target-profile> --verify
lark-cli auth status --profile <source-profile> --verify
```

If auth is missing or scopes are insufficient, use device-code login and guide the user to scan the QR code:

```bash
lark-cli auth login --profile <profile> --scope <comma-separated-scopes> --no-wait --json
lark-cli auth qrcode <verification_url> --output <relative-path.png>
lark-cli auth login --profile <profile> --device-code <device_code>
```

Use split-flow: generate a fresh authorization URL/QR code, send it to the user, then stop and wait for the user to say authorization is complete. Only after that run `lark-cli auth login --profile <profile> --device-code <device_code>`. Do not reuse old `device_code` values.

### Multi-Tenant Authorization Script

For each source tenant and the target tenant, repeat this checklist:

1. Tell the user which tenant is being authorized now.
2. Ask them to switch Feishu Web to the matching account before opening the authorization link:

   ```text
   现在要授权「<租户名>」。
   请先在浏览器打开飞书网页版，点右上角头像，确认当前登录/切换到「<租户名>」对应账号。
   如果网页端还停在别的租户，先退出或切换账号，再打开我发你的授权链接。
   ```

3. If they scan a QR code with the mobile app, remind them to confirm the mobile app is also on the matching account/tenant.
4. Generate authorization:

   ```bash
   lark-cli auth login --profile <profile> --domain drive,docs,wiki,sheets,slides,base --no-wait --json
   lark-cli auth qrcode <verification_url> --output <relative-path.png>
   ```

5. Send the authorization link and QR code. Ask the user to reply “已授权” after finishing.
6. After the user confirms, complete login:

   ```bash
   lark-cli auth login --profile <profile> --device-code <device_code>
   lark-cli auth status --profile <profile> --verify
   ```

Explain each QR step plainly:

```text
现在需要用“源租户”的飞书账号扫码。扫码后我才能读取这个租户的文档列表和导出内容。
```

For the target tenant, change the wording:

```text
现在需要授权“目标租户”。扫码后我才能在目标租户里创建文件夹、导入文档和上传文件。
```

Common scopes depend on content type. Start narrow, then add only when needed:

- Drive/document inventory and file export/import: Drive read/write scopes used by existing lark-cli drive commands.
- Modern docs: Docx document read where needed.
- Base/Bitable audit: Base app/table/block read scopes, especially when copy/export fails and you need to inspect structure.

Verify current scope behavior with `lark-cli` help and auth status because lark-cli evolves.

## Workspace Layout

Create one local workspace per migration:

```text
feishu-cross-tenant-migration-YYYYMMDD/
├── raw/
│   ├── inventory-<source>.jsonl
│   └── migration-events.jsonl
├── exports/
│   └── <source>/
├── final_summary.json
├── failed_latest.json
└── migration_manifest_latest.csv
```

Use relative paths when passing file paths to `lark-cli` from the workspace. Some commands reject absolute paths as unsafe.

## Inventory

Use Drive search for broad “my documents” inventory:

```bash
lark-cli drive +search \
  --profile <source-profile> \
  --mine \
  --query '' \
  --doc-types doc,docx,sheet,bitable,slides,file,wiki,folder \
  --page-size 20
```

Paginate with `page_token` until exhausted. Store raw results as JSONL before migration so the run is reproducible.

For folder- or wiki-scoped migrations, inspect the root link first:

```bash
lark-cli drive +inspect --profile <source-profile> <feishu-url-or-token>
```

Wiki links often wrap the real object. Unwrap them to the canonical object token before export/copy. Search results may expose this through fields like `icon_info.token`; inspect output shape instead of guessing.

Deduplicate using a stable key such as:

```text
(source_profile, source_token, source_url, title)
```

## Target Folder Setup

If the user does not provide a destination folder, create a target root folder in the destination tenant. Then create one child folder per source tenant/account:

```text
迁移总目录
├── 源租户A｜Markdown优先迁移
├── 源租户B｜Markdown优先迁移
└── 源租户C｜Markdown优先迁移
```

Keep folder names human-readable. Record target tokens and links in the manifest.

## Migration Strategy

Use this order unless a specific document type requires a fallback.

| Source type | First choice | Fallbacks | Notes |
| --- | --- | --- | --- |
| Modern docx / online docx | Export Markdown from source, import Markdown into target as online docx | Cross-tenant copy, then native docx export/import | Markdown-first generally preserves structure better than docx round-trip. |
| Legacy doc | Native doc/docx export, import as docx | Manual review or one-off copy if available | Legacy doc cannot use Markdown export reliably. |
| Wiki | Inspect/unwrap, then migrate underlying object by type | Recreate wiki structure after object migration | Do not migrate the wrapper token blindly. |
| Sheet | Cross-tenant copy | Native export/import if supported | Validate formulas and permissions by spot-checking. |
| Base/Bitable | Cross-tenant copy | `.base` export/import, then API audit and placeholder recreation if necessary | Some Bases cannot be exported/copied cross-tenant. |
| Slides | Cross-tenant copy | PPTX export/import | Spot-check layout. |
| Ordinary file | Cross-tenant copy | Download from source, upload to target | Preserve filename and extension. |
| Folder | Create target folder | Recurse contents if scoped by folder | Folders are structure, not content. |

### Markdown-First Documents

For modern Docx documents, prefer:

```bash
lark-cli drive +export \
  --profile <source-profile> \
  --file-token <source-token> \
  --doc-type docx \
  --file-extension markdown \
  --output <relative-path.md>

lark-cli drive +import \
  --profile <target-profile> \
  --folder-token <target-folder-token> \
  --type docx \
  --file <relative-path.md>
```

The key nuance: Markdown export uses `--doc-type docx`; Markdown import creates an online docx with `--type docx`.

### Legacy Doc Fallback

If the source is old `doc`, do not force Markdown. Use docx export/import:

```bash
lark-cli drive +export \
  --profile <source-profile> \
  --file-token <source-token> \
  --doc-type doc \
  --file-extension docx \
  --output <relative-path.docx>

lark-cli drive +import \
  --profile <target-profile> \
  --folder-token <target-folder-token> \
  --type docx \
  --file <relative-path.docx>
```

Mark these as `legacy_doc_docx_export_import` in the manifest.

### Base/Bitable Failure Handling

Try direct copy first, then `.base` export/import. If both fail, audit before creating a placeholder:

```bash
lark-cli base +base-get --profile <source-profile> --app-token <base-token>
lark-cli base +table-list --profile <source-profile> --app-token <base-token>
lark-cli base +base-block-list --profile <source-profile> --app-token <base-token>
```

If the Base has no tables/blocks or the API confirms there is no recoverable internal structure, create a same-name Base in the target and mark it clearly as a placeholder. Do not claim full migration. Include the reason in `notes`.

## Manifest Requirements

Write one JSONL event per attempted item as you work. At the end, derive latest-status files from it.

Recommended fields:

```json
{
  "source_name": "比白星辰",
  "source_profile": "cli_xxx",
  "source_type": "docx",
  "source_title": "Example",
  "source_token": "xxx",
  "source_url": "https://...",
  "target_profile": "feishu-new-tenant",
  "target_folder_token": "xxx",
  "target_token": "yyy",
  "target_url": "https://...",
  "status": "ok",
  "method": "markdown_export_import",
  "notes": "",
  "updated_at": "2026-06-12T10:00:00+08:00"
}
```

At completion, produce:

- `migration_manifest_latest.csv`: latest event per dedupe key.
- `final_summary.json`: counts by status, source, type, and method.
- `failed_latest.json`: latest failed/skipped items with reasons.

Use the bundled script if the JSONL fields follow the shape above:

```bash
python3 "/Users/fanhan/.agents/skills/飞书跨租户迁移文档@泛函/scripts/summarize_manifest.py" \
  raw/migration-events.jsonl \
  --out-dir .
```

## Reporting To The User

Keep final reports concrete:

```text
已完成迁移：
- 总计：725 个唯一源项目
- 成功：725
- 失败：0
- 主要方式：Markdown 导出再导入 572 个；跨租户直接复制 28 个；旧版 Docx 兜底 37 个
- 目标总目录：[迁移总目录](...)
- 本地清单：.../migration_manifest_latest.csv

需要注意：
- 旧版 Doc 走 docx 兜底，不是 Markdown。
- Base 如果 copy/export 都失败，我会先查结构；只有确认没有可迁移结构时才创建占位 Base。
```

Do not overwhelm a non-technical user with raw command output. Show only the decisions they need to understand or act on.

## Common Recovery Patterns

- Missing scope: stop, request QR authorization for the exact source or target profile, then resume the same item.
- `forbidden` on cross-tenant copy: switch to export/import fallback for that type.
- Markdown export unavailable: confirm the object is modern docx; if legacy doc, use docx fallback.
- Wiki token fails: inspect the wiki URL and migrate the underlying object token.
- Duplicate titles: keep both if source tokens differ; do not overwrite target files by title alone.
- Ordinary file too large: download/upload if copy fails; report if lark-cli returns a hard size limit.
- Interrupted run: resume from JSONL by skipping latest `status=ok` keys and retrying latest failures.

## When To Ask The User

Ask for help only when you need an action they can perform:

- Scan QR code with the correct Feishu account.
- Confirm which tenant/profile is the destination if names are ambiguous.
- Provide access to a private source folder/document that search cannot see.
- Spot-check proof-of-concept target links before a large migration.
- Decide whether placeholder Base creation is acceptable when real copy/export is impossible.

Everything else should be handled by the agent.
