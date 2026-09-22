# 高级交接：独立 Agnes + Hermes

这个模式用于已经熟悉 Agent、希望以后不再依赖 FirstWindow 日常操作的用户。

## 会创建什么

在 FirstWindow 的 **高级设置** 中点击 **配置独立 Agnes + Hermes**。

FirstWindow 会准备一个独立 Hermes profile：

```text
agneshermes
```

它和新手路径使用的 `firstwindowzero` 完全分开。

当前高级交接会配置：

- Hermes Agent 继续负责实际执行；
- Agnes `agnes-2.5-flash` 负责聊天、Coding、推理、Tool Calling 与图片理解；
- Agnes `agnes-image-2.1-flash` 作为 Hermes 原生生图 Provider；
- Agnes `agnes-video-v2.0` 作为 Hermes 原生生视频 Provider；
- 启用 Hermes `hermes-cli` 与 `video_gen` toolsets；
- 将模型 fallback 列表设为空，禁止静默切换其他模型 Provider。

Agnes API Key 必须由用户明确输入，只会保存到独立 `agneshermes` profile 的 `.env`。FirstWindow 不会从默认 Hermes 或其他 profile 复制 Key。

## 脱离 FirstWindow 直接使用

高级交接显示 **已配置** 后，可以关闭 FirstWindow，直接运行：

```powershell
hermes -p agneshermes chat
```

如果当前 Hermes/系统已经为该 profile 创建了 alias，也可能可以使用：

```powershell
agneshermes chat
```

验收时以 `hermes -p agneshermes ...` 作为标准启动方式。

## “已配置”到底证明了什么

FirstWindow 会在本地重新读取并检查：

- 独立 Hermes profile 确实存在；
- Agnes 已成为聊天 Provider；
- 聊天模型是预期 Agnes 模型；
- `fallback_providers` 为空；
- API Key 已存在于该独立 profile；
- Agnes 生图/生视频 Provider 插件文件存在；
- 两个媒体插件已启用；
- 生图/生视频模型配置正确；
- Hermes 所需 toolsets 已启用。

这属于 **配置级验收**。

它不等于“已经真实消耗一次图片/视频 API 并成功返回结果”。真实生图、真实生视频属于另外一层运行时证据，因为这些调用可能涉及配额或费用。

## 进阶以后，$0 边界发生什么变化

FirstWindow 新手路径有自己的 **$0 确认 + 实时通道防护**。

当你关闭 FirstWindow、直接运行原生 Hermes 后，**FirstWindow 的 $0 Guard 已经不在执行链中**。

独立 profile 仍然会阻止模型静默 fallback，但不能保证 Agnes 的生图/生视频调用永远免费。媒体 API 的可用性、配额和计费以当时 Agnes 账号/API Key 状态为准。

所以正确理解是：

```text
FirstWindow 新手模式
= 更强的成本/通道路由防护 + 恢复 + Evidence 验收

独立 Agnes + Hermes 高级模式
= 更自由的原生 Hermes 使用体验
  + 已预配置 Agnes 文本/视觉/生图/生视频
  - 不再由 FirstWindow 替你执行 $0 Guard
```

## 修复或重新配置

以后 Agnes/Hermes 配置变化时，可以重新打开：

**FirstWindow → 高级 → 配置独立 Agnes + Hermes**

该流程会修复专用 `agneshermes` profile，不修改 `firstwindowzero` 新手 profile，也不会复制其他 Provider 凭据。
