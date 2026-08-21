# Canva onboarding 与授权恢复

仅在 Canva 工具缺失、未连接、账号/团队错误或高级 Connect API 路径确实需要时读取。

## 先做最小探测

1. 在运行时检查是否存在 Magic Layers、设计导入、`get_design` 与 `get_design_pages` 能力。
2. 已连接时，优先执行只读设计查询或回读用户给定设计；不要为了“确认登录”创建垃圾设计。
3. Canva 工具缺失时，先用 Plugin Management 的当前能力发现/添加 Canva。若当前环境不能代为安装，指导用户在 Codex 的插件/应用设置中添加 Canva，然后回到同一任务继续。
4. 工具存在但返回 unauthorized 时，触发连接器授权，不直接创建开发者 integration。

Canva AI Connector 的功能会受方案、团队管理员、地区和 assistant 能力影响，必须运行时验证。[Canva AI Connector](https://www.canva.com/ai-connector/)

## 登录、团队与授权

- Canva 网页登录与 Codex 连接器 OAuth 是两个上下文。网页已登录或切团队，不证明连接器绑定到了同一账号/团队。
- 授权完成后，重新执行只读连接器调用。优先读取用户指定团队内的已知 design 或 folder；若连接器只返回 owner、不能证明 team，就在同一内置浏览器核验当前团队，再回到连接器读取该团队内已知资源。仍无法证明目标团队时，停止创建新设计。
- 若用户切换团队后仍读到旧团队内容，重新连接 Canva 插件，再验证；不要连续创建 Magic Layers 设计来试错。
- 必须走网页时，加载 `browser:control-in-app-browser`，只使用 Codex 右侧内置浏览器。完成必要 UI 步骤后回到连接器/API 回读验收。

## 密码、MFA 与验证码

- 密码、MFA、OTP、Authenticator code、CAPTCHA 都由用户在同一个右侧浏览器标签页手动输入。
- 不向用户索取这些值，不读取、不复制、不记录。
- 保留当前页面，等用户明确说“完成/继续”后再回读身份和授权状态。
- 不要把 MFA 当成普通插件连接的前置条件。只有登录页要求，或确实要创建 Canva Connect integration 时才进入 MFA 流程。

## 高级 Connect API onboarding

仅当连接器缺少导出、合并、页回读等本任务必需能力时使用：

1. 先确认账号可创建所需 integration；Canva 当前要求创建 integration 的账号开启 MFA。
2. 使用 OAuth 2.0 Authorization Code + PKCE(S256)。每次生成新的高熵 `state` 与 `code_verifier`，回调严格校验 `state`。
3. 本流程最小 scopes：`design:content:read`、`design:content:write`、`design:meta:read`。只有真的上传资产才增加 `asset:write`。
4. token 交换在本地后端完成。client secret、access token、refresh token 只留当前受控进程内存，不进浏览器、不打印、不写项目文件、不写长期记忆。
5. 读取响应中的 `expires_in`；不要硬编码 token 有效期。刷新时遵循 refresh token 轮换。

Merge 和 Get Design Pages 当前都属于 Preview；Public integration 的审核限制、字段、页上限与速率限制必须执行时查 changelog，不写死。

官方参考：[创建 integration](https://www.canva.dev/docs/connect/creating-integrations/) · [OAuth 与 PKCE](https://www.canva.dev/docs/connect/authentication/) · [Scopes](https://www.canva.dev/docs/connect/appendix/scopes/) · [Get design pages](https://www.canva.dev/docs/connect/api-reference/designs/get-design-pages/) · [Connect changelog](https://www.canva.dev/docs/connect/changelog/)

## Magic Layers 额度门

- Magic Layers 仍是动态可用的 AI 能力，且用量计入共享月度 AI allowance；方案、团队和管理员策略会影响可用性。禁止写死次数。[Magic Layers](https://www.canva.com/magic-layers/)
- 批量前先展示预计调用次数，先跑 1 页 pilot，再小批继续。
- API/job “completed” 只有同时返回真实 `design_id` 才算完成。
- 配额提示或 403 出现后立即停止；报告已完成页，不自动重试，也不建议绕过平台限制。
