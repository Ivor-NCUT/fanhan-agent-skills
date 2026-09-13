# 验收与交接

## 事实与内容

- `facts.json` 中每个主张都能回到源文件和行号。
- 没有把示意性 HR 消息、录取或业务结果写成承诺。
- `promo.json`、分镜和最终屏幕文字一致。
- 当前业务不需要的样片文字已经全部替换。

## HyperFrames

使用当前工程固定的 HyperFrames 版本：

```bash
npm install
npm run check
npm run render:draft
npm run render
```

修复所有 error；逐项查看 warning。对 3D 圆环等有意遮挡只能做窄范围标记，并用关键帧截图人工复核。

## 转场与画面

- 对每个场景边界抽取 `t-0.12、t-0.06、t、t+0.06、t+0.12` 五帧。
- 检查是否出现纯白/纯黑帧、整个窗口跳位、字体闪现、前后层同时透明或元素突然消失。
- 关键运动使用 HyperFrames keyframes strip 检查起点、中点和终点。
- 右侧网页、文件和通知在 9:16 成片中必须完整可读。

## 声音

- BGM 必须来自用户指定文件，并记录文件名、哈希和实际使用区间。
- 重要动作最多响应段落边界、downbeat 和高分 accent。
- 结尾不能硬切；通知音不得盖过音乐或与重音明显错位。
- BGM 权利范围不明时，在交接说明中标注“发布前确认版权”。

## 最小交付清单

- `facts.json`
- `promo.json`
- `storyboard.md`
- `assets/bgm.analysis.json`
- `keyframes/contact-sheet.png`
- `renders/draft.mp4`
- `renders/final.mp4`
- `qa-report.json`
- 完整可编辑工程

Skill ZIP 不包含用户 BGM、第三方参考视频、`node_modules`、缓存和临时帧。私人交接包可以单独附最终 MP4。
