# 飞书交接实测手册

验证日期：2026-10-21。CLI 1.0.97；通过已配置的 lark-cli 连接器执行，身份 user。以下占位符均须替换为本轮核实值，不把候选人个人信息写入 Skill。

## 发现与身份

先读取 lark-task、lark-shared；使用群消息时再读取 lark-im。连接器先调用 lark_status，再 lark_help 查询实际命令。CLI 等价命令：

```sh
lark-cli contact +search-user --query '<运营姓名>' --as user
lark-cli im +chat-search --query '<目标群名>' --as user
lark-cli im +chat-members-list --chat-id '<群ID>' --page-all --as user
```

同名联系人可能有多个账号。本次通过目标群成员的真实姓名、成员ID和既有运营任务交叉确认负责人。不要选第一个同名结果；负责人 open_id 和群 chat_id 放本地私有配置，每轮检查目标仍适用。

## 去重

```sh
lark-cli task +search --query '<完整联系方式>' --page-all --as user
lark-cli task +search --query '<小红书来源用户ID>' --page-all --as user
lark-cli schema task.tasks.get
lark-cli task tasks get --params '{"task_guid":"<命中GUID>"}' --as user
```

联系方式保留原文。手机号含空格时额外以去空格值搜索；大小写、下划线、短横线不得擅自改写。邮箱存在时亦查询完整邮箱。仅二维码则以来源ID及昵称辅助查询，不能编造微信号。

检索不加完成状态过滤，已完成任务也算既有交接。命中后读完整正文判断来源/岗位；本次两条历史命中凭完整联系方式加正文岗位一致，跳过新建。旧任务已完成但有新的追问，应向群报告并引用旧任务，不默认为再次加好友。

所有分页需确认 has_more=false；本地交接账本与远端搜索双重去重。搜索无结果不证明现实中未加好友，旧线索或我方曾说将添加的，任务注明先核实。失败读请求可以重试；写请求结果不确定时先回读，不盲目重建。

## 创建和验收

```sh
lark-cli task +create --as user --summary '<对接标题>' --description '<完整交接正文>' --assignee '<负责人open_id>' --idempotency-key '<稳定键>'
lark-cli task tasks get --params '{"task_guid":"<创建返回GUID>"}' --as user
```

本次创建键为 xhs-contact-<来源用户ID>-20261021；跨日仍必须先查账本及远端，不能靠带日期的键防跨日重复。后续应将完整来源ID+完整联系方式映射为稳定键，避免同一人更换联系方式被旧键吞掉；这是建议，尚未本轮实测。

正文包含：让运营用自己的号添加、昵称、来源用户ID/会话URL、岗位、联系方式原文、上下文、待核实点、回填添加进展。微信同号只在对方明确时写；类型不明明确待核实。企业招人写企业招聘对接、非候选人；项目合作明确合作诉求；图片二维码写打开来源扫描、无文字ID。不得承诺未经核实的公司、薪资、招聘资格或录用。

成功按 ok=true / exitCode=0 判断，不能要求旧式 code=0。创建后保存 GUID/URL，独立 get 回读，断言 description 完全一致且 members 中负责人 role=assignee、id为目标。任务创建不等于真实好友添加完成。

## 特殊情况群提醒

```sh
lark-cli im +messages-send --chat-id '<群ID>' --as user --text '<摘要与来源链接>' --idempotency-key '<稳定通知键，最多50字符>'
lark-cli im +messages-mget --message-ids '<返回message_id>' --as user
```

用户已明确授权的业务范围内发送；不要泛化到其他收件人。汇总非求职合作、企业招聘、无法添加格式、二维码、需要业务判断、旧任务后新追问等；不广播完整联系方式或无关个人材料。回读消息全文、群ID、deleted=false。平台风险提示只能称平台提示，不断言用户诈骗。

## 连接器参数与私有材料

上述 CLI 命令使用 lark_read/lark_write 的 command token 数组和 flags 数组，JSON 参数直接 JSON.stringify 对象，不用 shell 引号。大批独立查询可并行；创建和回读按依赖顺序执行。遇到高风险确认/权限错误遵守真实授权边界，不绕过权限。

仅私有工作账本保存候选人联系方式、来源ID、正文、GUID、去重证据及回读；不要放进公开 Skill 或 Git 仓库。公开 Skill 示例全部占位符。收件人配置单独保存在本地受限文件，公开包只给字段结构。
