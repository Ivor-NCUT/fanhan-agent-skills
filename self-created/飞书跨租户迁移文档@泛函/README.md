# 飞书跨租户迁移文档@泛函

用于把飞书 / Lark 云文档、知识库、云盘文件、多维表格、表格、幻灯片等资料从一个或多个租户迁移到目标租户。

## Files

- `SKILL.md`: 迁移主流程，包含非技术用户 onboarding、授权引导、Markdown 优先策略、各类型文档兜底方案。
- `scripts/summarize_manifest.py`: 根据迁移事件日志生成最终清单、失败列表和汇总统计。
- `evals/evals.json`: 基础测试提示词，覆盖全量迁移、Markdown 优先纠偏和 Base 授权卡点。

## Usage

安装到 Agent skills 目录后，当用户提出飞书跨租户迁移、文档搬家、创建副本、云文档归档等需求时自动触发。
