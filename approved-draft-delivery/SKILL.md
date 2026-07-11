---
name: approved-draft-delivery
description: Use this skill whenever the user approves, sends, retries, or checks delivery for an AI recruiting workbench email draft/outbox ID. It reads the exact approved SQLite outbox record, delegates real Feishu/Lark sending and send_status to the existing lark-mail Skill/CLI, then records message_id, delivery status, failure reason, timestamps, and attempt count back into opportunity_matcher. Never use it for unapproved drafts.
---

# 已批准邮件发送与投递回查

## Purpose

Complete the narrow handoff from a human-approved workbench outbox record to the existing `lark-mail` capability. This Skill does not write email copy and does not implement a mail client.

The workbench owns approval. `lark-mail` owns sending and `send_status`. The `opportunity_matcher` CLI owns deterministic outbox reads and delivery bookkeeping.

## Preconditions

1. The user instruction must identify one numeric outbox ID and explicitly state that it was approved, or explicitly ask to retry a previously approved/failed item.
2. Resolve the CLI project as in `daily-mail-ingestion`: use `./opportunity_matcher` when present, otherwise the current directory containing `src/opportunity_matcher`.
3. Read `lark-shared` and `lark-mail` before any mail operation.
4. Never send if the outbox record is absent or its status is not `approved`, `sent`, or `delivery_failed`.

## Read the exact record

From the CLI project directory:

```bash
PYTHONPATH=src python3 -m opportunity_matcher.cli \
  outbox --id <OUTBOX_ID> --json
```

Verify all of these against the current user-approved instruction:

- `id`
- `status`
- `recipient_email`
- `subject`
- `body`
- `attachments`

If recipient or subject differs from the approval instruction, stop and return the mismatch. Do not silently edit or send.

## Send through lark-mail

Use `lark-cli mail +send -h` to confirm the current attachment flags. Send as the authenticated user with the exact record fields and `--confirm-send`. Do not add recipients, CC, BCC, or attachments that are absent from the record.

If the send response contains an automation block reason, do not query `send_status`; record `blocked` with the exact reason.

If the send response contains a non-empty `message_id`, query real delivery status:

```bash
lark-cli mail user_mailbox.messages send_status \
  --as user \
  --params '{"user_mailbox_id":"me","message_id":"<MESSAGE_ID>"}'
```

Never fabricate a message ID or treat “command returned zero” as delivered.

## Record the result

For a new send or retry, include `--attempt`:

```bash
PYTHONPATH=src python3 -m opportunity_matcher.cli \
  record-outbox-delivery \
  --id <OUTBOX_ID> \
  --message-id '<MESSAGE_ID>' \
  --status delivered \
  --attempt \
  --json
```

Allowed recorded statuses:

- `pending`: accepted but recipient delivery is not final.
- `sent`: send API succeeded but no stronger recipient status is available.
- `delivered`: delivery status confirms success.
- `failed`: send or delivery failed; include `--error`.
- `blocked`: mail policy blocked sending; include `--error`.

For a later status-only recheck, omit `--attempt` so attempt count is not inflated.

## Failure and retry

- Before a mail request is made, do not increment attempt count.
- After a send request fails, record `failed --attempt` with a concise exact error.
- A retry still requires the user to identify the same approved/failed outbox ID.
- Re-read the outbox immediately before every retry; do not reuse stale recipient, subject, body, or attachment values from conversation history.

## Output

Return:

```markdown
## 邮件执行结果
- 草稿 ID：
- 收件人：
- message_id / draft_id：
- 投递状态：
- 尝试次数：
- 失败原因：
- 数据库回写：成功 / 失败
```

## Boundaries

- Do not send unapproved drafts.
- Do not draft or rewrite content in this Skill.
- Do not expose tokens, Keychain values, or raw credentials.
- Do not mark an item delivered without `send_status` evidence.
- Do not implement any of this workflow in the browser product.
