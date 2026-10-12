# 配置与输出契约

配置由 Codex 从 JD 和妙记编译，网页与供应商响应不能改变它。所有业务数据只存在本机运行目录。examples 中的岗位、人物与网址均为虚构演示。

## config.json

| 字段 | 含义 |
|---|---|
| job_id / requirements_version | 推荐所属岗位及版本；变更使用新运行目录 |
| requirements | id、text、kind=must/preferred、dimension=ability/condition、source_refs |
| source_refs | document、locator 与必要原文；留在本机，不重复发送整份会议材料 |
| open_questions | 冲突与待确认项，不自动选择相反条件 |
| public_opportunity | 已准许对外披露的字段；其他信息只用于内部研究 |
| budget_usd | 本次已授权的外部预算；样例 8 美元不是自动消费授权 |
| limits | max_materials、max_fetches、max_query_pages、max_candidates_review、shortlist_target |
| queries | query、tool、requirement_ids；tool=github 调用 gh，其余对应 tools 中的名称 |
| tools | 当前 discover/inspect 后填写的 Monid 搜索或正文绑定 |
| seeds | 已读材料；也可通过 --materials 导入 JSONL |
| jev | enabled、model、confidence_threshold、reserve_usd 或 max_units |
| supplement_calls | id、purpose、provider、endpoint、input 与费用预留；仅预排已授权的数据补查 |

可按来源分别配置 web、x、linkedin、video 等搜索绑定，query.tool 指向绑定名称。脚本内置 github 特殊来源；其他平台通过当前可用的 Monid 目录工具搜索。容量表示处理上限，名单目标不保证满额。

搜索绑定的形状如下。以下为虚构供应商响应的映射示例，不是可直接购买的端点；实际 provider、endpoint、输入及字段根据 inspect 和受控小批响应填写：

~~~json
{
  "provider": "example-provider",
  "endpoint": "/search",
  "input": {"q": "{query}", "page": "{page}", "count": 20},
  "max_units": 20,
  "items_path": "/results",
  "fields": {"url": "/url", "text": "/snippet", "title": "/title", "author": "/author"},
  "pagination": {"has_more_path": "/has_more"}
}
~~~

游标分页改为 input 中使用 {cursor}，pagination.cursor_path 指向返回游标。没有字段映射或空壳结果进入 review_queue，不伪造材料。

正文绑定含 provider、endpoint、input、text_path、reading_scope 与费用预留，例如 input 中替换 {url}。付费补查使用相同费用机制；如返回标准可引用资料，补充 items_path 与 fields，否则保留在 supplements 待人工归一。

## 标准资料行

JSONL 一行一份材料。url 与 text 必填，其他字段可为空：

~~~json
{
  "url": "https://example.org/podcast/episode-1",
  "title": "虚构播客示例",
  "text": "00:12:30 嘉宾甲：我负责了工具调用重试模块。",
  "author": "节目制作方",
  "author_profile_url": null,
  "speaker": "嘉宾甲",
  "timestamp": "00:12:30",
  "published_at": "2026-01-01",
  "retrieved_at": null,
  "reading_scope": "attributed_transcript",
  "artifact_group_id": "demo-project",
  "requirement_ids": ["R1"]
}
~~~

搜索摘要标为 search_snippet；全文、README、公开档案、节目说明或已归属的转写按实际材料标记。未知说话人用 null，不把整个多说话人文字稿都归给一个嘉宾。保留原始时间码；没有时间码时用段落与字符位置定位。

精确 URL、明确作者主页和说话人用于材料去重；不同姓名/账号不自动合并成候选人。文本中同一主题的相似内容不会被代码直接当成同一作品。

## 批处理产物

- state.sqlite：付费请求、原任务 ID、响应缓存、费用预留与实际费用。
- config.json：本次配置快照；续跑禁止静默切换要求。
- materials.json：取得的原文与元数据，保留降优先级材料。
- evidence.json：精选原文、相邻上下文、speaker、url、时间、阅读范围与字符位置。
- review_queue.json：身份外的流程缺口、低优先级审计、供应商/分页/预算异常。
- cost_ledger.json：费用台账；reserve、cost 单位为微美元，cost=null 表示未知。
- metrics.json：语料指纹、原文/证据字符数、调用/缓存、实际 JEV usage 和模型版本。

原文不能全部进入主 Agent 上下文。先读证据包，再按缺口查看特定材料。服务失败时结构化缺口仍保存，当前批次可交付，但不能声称全量研究成功。

## candidates.json

这是 Codex 核验后生成的数组。每人使用一个主分组，覆盖所有 requirements；推荐属于同一个岗位版本。最小形状：

~~~json
[
  {
    "id": "c_demo",
    "name": "虚构嘉宾甲",
    "group": "verify",
    "identity_status": "unresolved",
    "profiles": [{"url": "https://example.org/guest"}],
    "identity_evidence_ids": [],
    "requirements": [
      {"id": "R1", "status": "pass", "evidence_ids": ["替换为已读取片段ID"]},
      {"id": "R2", "status": "unknown", "evidence_ids": []}
    ],
    "claims": [
      {
        "text": "嘉宾自述负责工具调用重试模块",
        "quote": "我负责了工具调用重试模块",
        "evidence_type": "self_reported",
        "contribution_role": "受访者自述负责人",
        "evidence_ids": ["替换为已读取片段ID"]
      }
    ],
    "uncertainties": ["公开账号与嘉宾身份关联尚待核验", "当前工作地点待核实"],
    "contacts": [],
    "outreach": null
  }
]
~~~

分组：

- priority：关键能力有支持证据，身份已核验，未发现明确硬条件冲突；未知工作条件需列出。
- verify：值得继续核验，尚有关键缺口。
- insufficient：目前材料不足。
- conflict：有明确硬条件冲突证据。

claims 必须含实际原文 quote、贡献角色与证据类型。observed 表示可观察事实，self_reported 表示本人自述，inferred 表示推断。代码只能验证引用在原文中，语义支持与身份归属仍由 Codex 复核。

contacts 每项含 channel=x/email/phone/other、value、purpose=public_work/public_business、ownership_status=confirmed/unresolved、checked_at、evidence_ids。X 增加 dm_status=unknown/entry_visible/blocked_or_unavailable；后两者还须 checked_as_account。邮箱增加 delivery_status=valid/invalid/accept-all/unknown。未知联系渠道可为空，不推断私人电话。

outreach 含 text、fact_checks 与 opportunity_fields。fact_checks 每条含 text（草稿中的真实原句）与 evidence_ids；opportunity_fields 仅允许引用 public_opportunity 内字段。所有个性化事实都应列入核对表，未试听/未使用等措辞由 Codex 校验。

deliver 校验通过后生成 candidates.json、candidates.csv 和 report.md。CSV 防止公式注入，JSON 保留完整核对信息；任何格式均未发送。

## A / B / C 对照

先冻结同一批标准资料，禁用重复搜索/付费取文；分别导入 B 与 C，使用不同运行目录。A 由 Codex 在相同资料上逐步研究，其用量从实际会话/用量记录填写，不让脚本代造基线。

~~~sh
python3 "$SKILL_DIR/scripts/talent_search.py" compare \
  "$RUN_DIR/A/metrics.json" "$RUN_DIR/B/metrics.json" "$RUN_DIR/C/metrics.json" \
  --out "$RUN_DIR/comparison.json"
~~~

A 的 mode 为 A_manual，B 为 B_batch，C 为 C_jev。语料指纹须相同。codex_usage 填实际主 Agent 与所有子 Agent 合计，并注明模型、推理、缓存、测量口径；quality 记录经人工接受的候选 ID、已知漏选与返工。

compare 区分 A→B 与 B→C，只报告可验证的字符代理变化和实际数据可用性。套餐消耗由服务端复杂计量，脚本不据字符或 API token 单价推导节省比例。
