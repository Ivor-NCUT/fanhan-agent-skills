---
name: ai-design-import-canva-fanhan
description: Import external or AI-generated flat designs into Canva with account onboarding, Magic Layers conversion, ordered multi-page assembly, and page-by-page fidelity checks. Use when the user provides PNG, JPEG, WEBP, HTML, or SVG files and wants editable Canva pages or one verified multi-page Canva design. Do not use for ordinary edits to an existing Canva design, generating a new design from a brief, uploading an image only as an asset, resizing, brand review, or template autofill.
---

# AI 设计导入Canva@泛函

把“排版不乱”落实成硬验收门：未通过页数、尺寸、顺序、视觉、图层和文字检查，就不交付最终 Canva 链接。

## 输出约定

默认交付一个 Canva 设计，并报告：

- 编辑链接与 `design_id`
- 最终页数、每页尺寸与顺序
- 每页来源及处理路线
- 可编辑图层 / 整页扁平化状态
- OCR 错字、字体替换或其他仍存在的例外

视觉一致和文字可编辑是两项独立指标。Magic Layers 看起来正确，不代表拆出的文字没有错字。

## 工作流

1. 盘点输入。按自然数字顺序建立页面清单，记录文件、宽高、比例、目标页码和是否含外部字体/资源。
2. 检查所有页是否同像素尺寸、同方向、同宽高比。即使都为 3:4，只要像素尺寸不同，也要先确定唯一 `target_width × target_height`，再逐页显式 `fit`、`crop` 或重渲染；绝不让 Canva 隐式缩放。混合比例时停止自动合并，只问用户选择 `fit`、`crop` 或按尺寸分组。
3. 运行时探测 Canva 插件工具与连接状态。缺插件、未授权、账号/团队不对或出现 MFA 时，读取 [onboarding.md](references/onboarding.md)。
4. 按下表选最短且最保真的路线。Magic Layers 只处理栅格图；HTML/SVG 是否先栅格化取决于用户更看重视觉一致还是结构可编辑。
5. 先处理一页代表性素材。只有返回真实 `design_id`，且回读设计成功，才继续批量。任务状态为 completed、出现配额文案或只返回 widget 都不算成功。
6. 分批处理其余页面，并维护 `source file -> source design_id -> final page` 台账。每次 Magic Layers 调用都会新建设计，不能复用旧 widget 或上一批的 ID。
7. 需要多页聚合时读取 [import-and-merge.md](references/import-and-merge.md)。优先复用已有 Canva 插件和官方 API；只有能力缺口才用 Connect API 或内置浏览器。
8. 执行全部质量门。失败时只重做出问题的页；修复后重新跑最终整套验收。
9. 清理本轮生成且可重新生成的临时 PNG、PPTX、渲染图和 OAuth 进程；不得删除源文件、最终交付物、凭据或不明共享缓存。

## 输入路由

| 输入与目标 | 路线 |
|---|---|
| PNG/JPEG/WEBP，要拆成可编辑元素 | `canva_image_to_design`（Magic Layers） |
| 图片只需保存为 Canva 素材 | 退出本 Skill，使用 Canva 资产上传能力 |
| 图片只是风格参考 | 退出本 Skill，使用 Canva 设计生成能力 |
| 静态 HTML，优先保留 DOM 结构 | 规范化为自包含 HTML/ZIP，再原生导入 Canva |
| HTML 必须统一经过 Magic Layers | 固定 viewport 无损渲染为 PNG，再逐页 Magic Layers |
| SVG，优先保留矢量外观 | 包进固定尺寸、自包含 HTML 后原生导入并验收 |
| SVG，优先拆层或原生导入失真 | 按目标尺寸高分辨率渲染为 PNG，再 Magic Layers；不承诺每个 path 都成为 Canva 矢量元素 |
| 混合格式、多文件合成一份 | 先逐页规范化并建立台账，再按高级聚合路线合并 |

当前工具名和支持格式可能变化。每次都从运行时工具说明确认，不把本文件当作 API schema。

## Canva 调用规则

- 优先级：Canva 插件/连接器 → 官方 Connect API → Codex 右侧内置浏览器。
- 只有用户已经提供公开 HTTPS URL 时才传 `url`。平台文件或本轮生成 artifact 使用 `image_file` / `design_file`。
- 禁止为了拿 URL，把本地、私有或 agent 生成文件上传到临时图床或公开文件托管。直接文件传输不可用时，让用户在 Magic Layers tile 或 Canva 原生上传界面手动选文件。
- 批量开始前说明预计 Magic Layers 调用次数：`待拆层图片数 N ≈ N 次调用 / N 个新设计`。额度是动态的，不声称具体余额。
- 遇到配额提示、403、缺失 `design_id`、错误账号/团队或授权失效，立即停在已验证页，不循环重试消耗额度。
- 不从别的批次复用 `design_id`，也不把“API job success”当成结果正确。

## 硬质量门

### 源页

- 每个 Magic Layers 结果都有新的真实 `design_id`，能用 `get_design` 回读，且 `page_count=1`。
- 页面缩略图与源图同尺寸/同宽高比；检查裁切、字体替换、文本换行、元素位移和背景缺失。
- 使用只读内容能力回读文字。完整元素结构只有在运行时工具明确返回时才可据此判断；必要时打开编辑事务读取 richtexts/fills/元素且不做修改，随后立即取消事务。若无法结构化证明，就标记“可编辑性未验证”，不能宣称可编辑或整页扁平化。

### 合并中间件

- 若经过 PPTX，调用 `presentations:Presentations` 复用其导入现有 deck、合并、逐页渲染和 overflow/overlap 检查；不要用 `python-pptx` 重建页面。
- 合并前后页数、页序和页面尺寸完全一致。每一轮转换后都重新渲染，不沿用上一轮截图。

### 最终 Canva 设计

- `get_design` 返回 `page_count = 预期 N`。
- 以 `page_count` 为目标，用 `offset` / `limit` 循环调用 `get_design_pages`，直到收齐 N 页；按页码去重并确认 `1..N` 无缺失、无重复，再逐页核对尺寸、方向、顺序和缩略图。REST 响应优先读取当前 schema 的 `page_number`，不要依赖已弃用字段。
- 先把最终页与源图归一化到同一像素尺寸，再做像素或感知相似度检查和逐页视觉检查。自动阈值只用于筛查，不能替代肉眼检查；阈值应由 pilot 和目标保真度确定，不写死一个通用数值。
- 对照源文字检查 OCR。任何错字必须修复或在交付中明确列出，不能用“视觉一致”掩盖。
- 最后在 Canva 编辑器检查每一页的实际渲染和可编辑性。只在页数、尺寸、顺序、视觉均通过后称为“排版未紊乱”。

## 停止条件

以下任一项成立就暂停交付并报告已完成页和确切阻塞：

- 用户尚未决定混合比例的处理方式
- 插件连接到了错误账号或团队
- 需要用户手动输入密码、MFA、OTP 或验证码
- Magic Layers 额度不足或某页没有真实 `design_id`
- Merge/Import 显示成功但最终页数、顺序或尺寸不符
- 任一页出现明显排版偏移、裁切、字体替换或未披露的 OCR 错字

## 与其他 Skill 的边界

- 已有 Canva 设计的文字/素材修改：`canva:canva-edit-design`
- 从 brief 新建设计或品牌演示：Canva 生成/品牌演示 Skill
- 数据批量套模板：`canva:canva-bulk-create`
- 本地 PPTX 的独立创建/编辑：`presentations:Presentations`
- 插件发现与安装依赖：`plugin-management:plugin-management`
- 登录、授权、MFA、原生文件上传和最终页面验收：`browser:control-in-app-browser`
- 临时产物收尾：`task-artifact-cleanup`
