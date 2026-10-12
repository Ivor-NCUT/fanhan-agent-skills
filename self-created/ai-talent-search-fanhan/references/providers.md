# Monid 与 JEV 接口

以下合同于 2026-10-12 核实；目录、报价、字段和模型别名继续以运行时 inspect 为准。仅链接官方资料，不复制供应商 Skill 或 SDK。

- [Monid Discover](https://docs.monid.ai/api/discover.html)：POST /v1/discover，query 与 limit，搜索的是可用工具。
- [Monid Inspect](https://docs.monid.ai/api/inspect.html)：POST /v1/inspect，provider 与 endpoint；返回 inputSchema、price、usage 与文档。
- [Monid Run](https://docs.monid.ai/api/run.html)：POST /v1/run，provider、endpoint、input；同步返回结果或异步 runId。
- [Monid Runs](https://docs.monid.ai/api/runs.html)：GET /v1/runs/{runId}；核对生命周期、providerResponse.httpStatus、output 与实际账单。
- [Monid Pricing](https://docs.monid.ai/guide/pricing.html)：报价单位可能是调用、结果或其他使用量；不能把 PER_RESULT 单价当成每次费用。
- [Monid 的 Jev 实跑](https://monid.ai/blog/guides/llm-as-a-judge-typesafe-jev)：typesafe /systemone，正文是 state、model、questions。
- [TypeSafe API](https://docs.typesafe.ai/api) 与 [Choice](https://docs.typesafe.ai/primitives/choice)：每个问题使用 type、instructions、criteria；返回 answers 下的 choice、probabilities 与 confidence。JEV 返回判断，不生成开放文本。

## 认证

唯一付费入口为 https://api.monid.ai。脚本从 MONID_API_KEY 环境变量读取密钥；也可读取 ~/.config/ai-talent-search-fanhan/credentials.json，内容为：

~~~json
{"MONID_API_KEY": "在本机填写"}
~~~

凭据文件权限须为 600，不接受符号链接。也可用全局参数 --credentials 指定受限文件。密钥不放进 config.json、命令参数、Skill、测试、GitHub、报告或聊天正文。脚本拒绝重定向，避免把认证头带到其他主机。

doctor 只检查配置是否存在，不代表 API 授权或付费额度已通过。用户提供配置并授权本次预算后，先 discover / inspect，再进行受控真实调用。

## 工具绑定

每个 Monid 工具写明 provider、endpoint、input。查询变量为 {query}、{page}、{cursor}；正文变量为 {url}。只替换字符串，不执行模板代码。

搜索映射使用 items_path 与 fields，路径为 JSON Pointer，根值用空字符串。正文接口使用 text_path。字段由当前 inspect 和小批实际响应决定。供应商 schema 由 Monid 验证；本脚本不声称实现完整 JSON Schema 校验。

分页可配置 cursor_path 和 has_more_path。输入对应字段使用 {cursor} 或 {page}。重复游标、缺少下一游标、上限和异常进入复核队列，保留当前数据。

补查可通过 supplement_calls 批量预排职业资料、公开联系渠道、字幕等查询；未有来源 URL 的结果保留为原始补查资料，不能直接当作可引用证据。转换为标准资料行后再次导入，或用 fields 自动映射。付费转写的原始音频获取须另外授权，首版不自动下载音频。

## 费用与重试

SQLite 在提交前预留费用。PER_CALL 根据当前报价；PER_RESULT 用 max_units × 单价加基础费。其他计费方式须提供 reserve_usd 并核对当前计费说明。JEV 建议先设每批 0.02 美元预留额，再按实际 usage 与账单校准；这不是实时单价声明。

供应商实际费用回读后替换预留额；没有实际账单时继续占用预留额。应用层停止新请求，**不能保证供应商最终账单不超过预留额**。变化的单价、计费数量或未知账单会被保留；已超预算时停止后续新提交。

提交请求超时、断网或缺少 runId 时不自动重提。状态可查时只轮询原 runId，暂时查询失败可有界重试。若提交是否发生不明，去 Monid 任务/账单核对；取得精确 runId 后运行：

~~~sh
python3 "$SKILL_DIR/scripts/talent_search.py" reconcile \
  --directory "$RUN_DIR/batch" --request-key REQUEST_HASH --run-id VERIFIED_RUN_ID
~~~

此命令回读并要求 provider、endpoint、input 与原请求一致。匹配后续跑原配置。无法确认时该请求继续保留，不用“失败”推断为“未收费”。

## JEV 版本与验证

jev-latest 方便首轮接入，别名会改变；对照实验应记录响应中的实际 model，必要时固定已验证模型 ID。批处理共享岗位摘要；原文保留本地，精选片段按原始字符位置复制。confidence 门槛须在目标中文/英文材料上校准。

首版不安装 TinyFish、Actionbook 或第二个浏览器。复杂网页成为明确瓶颈时再按用户环境接入。脚本不能读取 Codex 内置浏览器登录态，登录与验证码由用户在同一内置页完成。
