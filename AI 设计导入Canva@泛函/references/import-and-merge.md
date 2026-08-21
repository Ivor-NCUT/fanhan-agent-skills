# 输入规范化与多页聚合

## 图片与 Magic Layers

当前 Canva 插件的 Magic Layers 原语是 `canva_image_to_design`，运行时以工具 schema 为准：

- 适合 PNG/JPEG/WEBP 的海报、横幅、传单、社媒图等扁平设计。
- 写实照片可以尝试，但必须提示拆层质量通常更不稳定。
- `image_file`、`server_img_id`、公开 `url` 三选一。
- 每次调用都是独立工作流并创建新的 `design_id`。先 pilot，再按页面顺序分批；每页成功后立即回读并写入台账。
- Magic Layers 是 Canva 插件/AI Connector 能力，不是公开 Connect REST endpoint。

## HTML

HTML/SVG 都按未受信任输入处理。预检并移除或拒绝 `script`、内联事件处理器、`iframe`、`foreignObject`、表单、自动导航和未获用户授权的远程资源；在隔离、禁网、不能读取本地凭据的环境中渲染。若这些主动能力是用户设计的必要部分，停止本导入流程并先确认安全边界。

优先结构可编辑时：

1. 做成自包含 HTML 或 ZIP：固定像素宽高；只内联或打包已核验资源；等待字体/图片 ready；禁用动画、过渡、计时器和 viewport 依赖。
2. 静态多页文件的每个顶层页面元素添加 `data-document-role="page"`，页面之间不可嵌套；可加 `data-label` 和 `data-speaker-notes`。
3. 使用运行时 `canva_import_design_from_url` 的 `design_file` 导入本轮生成/上传的 HTML/ZIP，或对用户已提供的公开 HTTPS URL 使用 `url`。
4. 导入后仍执行全部最终质量门。HTML 支持属于当前连接器能力，不能假定 Connect REST `/imports` 同样支持。

必须统一经过 Magic Layers 时：按每页目标尺寸在固定 viewport 上无损渲染为 PNG，资源和字体完全加载后再逐页调用 Magic Layers。

## SVG

1. 先检查明确的 `width`、`height`、`viewBox`，并内联外部图片、字体和样式。
2. 优先保留外观时，把 SVG 放入同尺寸自包含 HTML 后原生导入。
3. 原生导入出现滤镜、字体、裁切或定位差异，或用户明确要 Magic Layers 时，按目标像素尺寸渲染成无损 PNG，再走 Magic Layers。
4. 不承诺每个 SVG path 都成为 Canva 可编辑矢量。Connect Assets API 当前也不能作为 SVG 上传的通用替代。

官方格式边界：[Design imports](https://www.canva.dev/docs/connect/api-reference/design-imports/) · [Connect assets](https://www.canva.dev/docs/connect/api-reference/assets/) · [Apps SDK assets](https://www.canva.dev/docs/apps/uploading-assets/)

## 多页聚合优先级

### A. 已经是一个多页 HTML/ZIP

直接原生导入为一个设计，避免先拆成 N 个 Magic Layers 设计再合并。只有用户明确要求每页都做 AI 拆层时才走逐页路径。

### B. Connect Merge API（可选优化）

仅在已有合格 Connect OAuth、输入是 fixed pages 且运行时仍支持时尝试。Merge 是 Preview；Get Design Pages 同样是 Preview。先查 changelog、Public integration 限制与当前 schema。

- 一个请求只放一个 operation。
- 首页用 `create_new_design`；其余逐页 `modify_existing_design` + `insert_pages` 追加。
- 每个 job 轮询到终态后，立刻 `get_design` / `get_design_pages` 验证页数实际增加、顺序和尺寸正确。
- `status=success` 但页数未变属于失败，立即转 C 路线；不要继续追加。

官方参考：[Create design merge job](https://www.canva.dev/docs/connect/api-reference/merges/create-design-merge-job/)

### C. PPTX round-trip（可靠 fallback）

1. 对每个 source design 先查可用 export formats；只有支持 PPTX 才创建导出 job。下载 URL 有时效，立即下载到任务临时目录。
2. 调用 `presentations:Presentations` 导入每个现有 deck，按台账顺序复制原页并合并；保留现有对象，不用 `python-pptx` 重建。
3. 逐页 render，运行 overflow/overlap 测试，确认页数、尺寸、顺序和文字换行。
4. 将合并 PPTX 导回 Canva。公开 HTTPS 用 connector；私有本地 PPTX 若 `design_file` 不支持，就用 Codex 内置浏览器在 Canva 原生上传，绝不临时公开托管。
5. Design Import 可能返回多个 designs；必须检查 `result.designs` 数量。导入后重新执行完整 Canva 质量门。

官方参考：[Export job](https://www.canva.dev/docs/connect/api-reference/exports/create-design-export-job/) · [Export formats](https://www.canva.dev/docs/connect/api-reference/designs/get-design-export-formats/) · [Import job](https://www.canva.dev/docs/connect/api-reference/design-imports/create-design-import-job/)
