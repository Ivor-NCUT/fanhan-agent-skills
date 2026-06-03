# Feishu/Lark Course CLI Patterns

Use this reference for the `lark Course 协作` workflow.

## Read

Resolve wiki nodes first when the URL is `/wiki/<token>`:

```bash
lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'
```

Fetch readable Markdown:

```bash
lark-cli docs +fetch --api-version v2 --doc "<url-or-token>" --doc-format markdown --detail simple
```

Fetch block IDs for comments:

```bash
lark-cli docs +fetch --api-version v2 --doc "<url-or-token>" --doc-format xml --detail with-ids
```

Do not mix `--detail with-ids` or `--detail full` with Markdown.

## Write

Overwrite the current course doc when direct editing is intended:

```bash
lark-cli docs +update --api-version v2 --doc "<url-or-token>" --command overwrite --doc-format markdown --content @draft.md
```

Create a sibling doc only when the user explicitly asks not to touch the original. Use the resolved parent node token and current CLI docs create reference.

## Comment

Add a local comment to a docx/wiki paragraph block:

```bash
lark-cli drive +add-comment --doc "<wiki-or-doc-url>" --block-id "<block_id>" --content '[{"type":"text","text":"AI Check：..."}]'
```

The flag is `--doc`, not `--file`.

If a quote, container, or unsupported block fails with "specified block does not support comments", anchor the comment to the child paragraph block inside it.

Verify comments:

```bash
lark-cli drive file.comments list --params '{"file_token":"<docx_token>","file_type":"docx","is_solved":false}'
```

## CEO Review Queue

From the Agent Native root, the `CEO 审查队列表` is a bitable. Resolve it by wiki tree when possible rather than requiring global search scope.

Typical current shape:

- Base token: resolved `obj_token` of `CEO 审查队列表`
- Table name: `审查队列`
- Fields include `产出名称`, `产出类型`, `审查状态`, `最终版本链接`, `需要 CEO 判断的点`, `修改意见`, `提交时间`, `AI 自评分`

Always read table and field structure before writing:

```bash
lark-cli base +table-list --base-token <base_token>
lark-cli base +field-list --base-token <base_token> --table-id <table_id>
```

Create the record:

```bash
lark-cli base +record-upsert --base-token <base_token> --table-id <table_id> --json '{...}'
```
