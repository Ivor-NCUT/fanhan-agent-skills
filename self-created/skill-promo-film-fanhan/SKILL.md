---
name: skill-promo-film-fanhan
description: 根据 Agent Skill 仓库与用户指定的 BGM，制作或迭代 9:16 Codex 浅色苹果式代码动画宣传片，并交付可编辑 HyperFrames 工程、关键帧和 MP4。Use when the user asks to make a Skill 预告片、宣传动画、Codex UI 动画，或沿用这套风格修改已有成片；不用于真人录屏剪辑、口播包装或自动联网选歌。
metadata:
  version: 0.3.0
---

# Skill 动画宣传片@泛函

把一个真实 Agent Skill 转成一条短、清楚、可继续修改的产品动画。技术生成由本 Skill 负责；故事、文案和具体动效反馈以用户判断为准。

## 输入与完成标准

必须取得：

- 目标 Skill 的目录、`SKILL.md` 或仓库。
- 用户选定的 BGM 文件。不要擅自联网选歌。

剧本是可选但优先级最高的输入。目标 Skill 和 BGM 已提供、但用户尚未说明是否有剧本时，只问一次：

> 如果你有剧本的话，可以给我；没有的话，我就基于这个 Skill 自己思考并生成一版。

等待用户回答后继续。用户提供剧本时锁定其核心故事、角色关系和信息顺序，只修正事实错误、不可实现内容与明显超时；没有剧本或用户明确让 AI 决定时，按 [故事语法](references/story-grammar.md) 自行构思，不再追问。用户已经给齐输入或明确授权继续时直接制作，不设置重复确认门槛。

还可以使用：参考视频、产品截图、演示 GIF、品牌素材和上一版工程。

一次完整交付至少包含：事实清单、分镜表、音乐节奏分析、关键帧总览、低清预览、最终 MP4、可编辑 HyperFrames 工程和 QA 报告。

## 工作流

1. **建立事实源**
   - 完整读取目标 `SKILL.md`，按需读取 README、references、演示 GIF 和真实输出。
   - 生成 `facts.json`：每个宣传主张都记录源文件、行号和原文；未经证实的效果只能作为剧情化示意，不能写成产品承诺。

2. **创建或续接工程**
   - 有剧本的新工程运行：`node <本Skill目录>/scripts/create-project.mjs --skill <Skill路径> --music <BGM路径> --script <剧本.md> --output <输出目录>`。
   - 没有剧本时省略 `--script`；脚手架会把模式记录为 `agent-generated`，随后必须依据事实源自行生成，不能沿用样片剧情。
   - 已有 HyperFrames 工程则原地迭代，不重新脚手架。
   - 脚手架复制的求职内容只是风格样片，必须依据当前 Skill 重写，不得把简历、JD、HR 固定成通用剧情。

3. **设计单线故事**
   - 有用户剧本时先核对事实并忠实转成分镜；不要擅自换故事。无剧本时阅读 [故事语法](references/story-grammar.md)，围绕一个用户任务建立因果链，不做功能宫格或平均分配的功能巡展。
   - 把逐镜内容、屏幕文案、动效、时长、音乐依据和事实 ID 写入 `storyboard.md` 与 `promo.json`。

4. **让音乐先进入时间轴**
   - 调用 `$music-animation-analyzer` 分析用户指定的 BGM；严格使用其真实时间戳。
   - 用段落边界、downbeat 和高分 accent 安排重要转场；普通 beat 只驱动轻微响应，不能每拍切镜头。
   - 用户指定截取区间时遵从；否则选覆盖完整故事且结尾自然的片段，并做短淡入、末尾淡出。

5. **生成 Codex 浅色动画**
   - 先调用 `$hyperframes`，按需加载其 core、animation、keyframes、audio、registry 和 CLI 能力。
   - 写任何 GSAP/CSS/Canvas 动效前，读取内嵌的 [motion-web](vendor/motion-web/SKILL.md)，并至少读取其 [build-mode](vendor/motion-web/references/build-mode.md)、[motion-tokens](vendor/motion-web/references/motion-tokens.md)、[handfeel](vendor/motion-web/references/handfeel.md)、[timeline-orchestration](vendor/motion-web/references/timeline-orchestration.md)、[verification-harness](vendor/motion-web/references/verification-harness.md)、[design-slop](vendor/motion-web/references/design-slop.md) 与 [scene-audio](vendor/motion-web/references/scene-audio.md)。
   - `motion-web` 只负责运动物理、手感、编舞、静帧审美闸门和可验证性；不要套用其网页信息架构、案例皮肤或营销站视觉。产品界面仍以本 Skill 的 Codex 浅色契约为最高优先级，渲染仍由 HyperFrames 完成。
   - 复用上游案例的机制时必须先读对应 `README.md` 的“可以照搬/不许照搬”；只取机制，不复制配色、字体、文案和版式。
   - 阅读 [视觉与动效契约](references/style-contract.md)，以 `assets/codex-light-template/` 为风格和实现参考。
   - UI、文字、文件和网页全部用可寻址 DOM 元素实现；不用真实 Codex 录屏。

6. **审片与迭代**
   - 先生成关键帧接触表，再生成 draft MP4。用户指出某一帧、某段文字或某个动效时，只修改对应内容，保留已经认可的镜头。
   - 文字修改优先落到 `promo.json`；时间修改落到时间轴；不要为局部反馈推倒整片。

7. **验证和交付**
   - 运行 `node <本Skill目录>/scripts/test-create-project.mjs`，再按 [0.2 验收用例](references/acceptance-cases.md) 和 [验收与交接](references/qa-and-handoff.md) 完成输入模式、事实、布局、转场、音乐和输出检查。
   - 如果使用了内嵌 `motion-web` 案例机制，运行它对应的无头验证判据；若只使用原则，则把采用的 motion token、交接锚点和验证结果写入 `qa-report.json`。
   - BGM 版权未确认时只放入私人项目和最终成片，不放进公开 Skill 包或仓库。

## 固定边界

- 默认竖屏 1080×1920、中文、Codex 浅色界面；除非用户明确要求其他画幅或语言。
- 用户输入使用光标打字机；AI 输出使用逐字淡入。
- 不使用蓝色点击圆圈、鼠标录屏提示环、无意义粒子或装饰性科技光效。
- 转场必须保留连续视觉锚点，不能让相邻场景同时降到透明而露出白底。
- 不固定时长，不固定镜头数，也不固定“安装 Skill—JD—简历—HR”剧情。
- 不把 AI 自行生成的剧本冒充用户确认稿；`promo.json` 必须记录 `scriptMode`。
- 这是一条预告片；真实操作教程和真人投屏演示应单独制作。
- `motion-web` 的“整站构建”输出契约不适用于本 Skill；不要因此把宣传片改造成滚动网站。

## 来源与许可

需要公开、分发或打包时先阅读 [来源与许可](references/sources-and-licensing.md)。
