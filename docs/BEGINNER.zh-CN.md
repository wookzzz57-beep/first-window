# FirstWindow 新手教程

[English](BEGINNER.md) · **简体中文**

> **目标：** 不需要先学 Coding Agent 的底层概念，也能完成第一个任务。

正常的 Windows 使用流程**不需要终端**。Provider 配置、通道检查、断点恢复和验收逻辑由 FirstWindow 在应用里处理。

## 5 分钟快速开始

<!-- QUICKSTART:START -->

1. **下载 FirstWindow**  
   下载 [FirstWindow-Windows-x64.exe](https://github.com/wookzzz57-beep/first-window/releases/latest/download/FirstWindow-Windows-x64.exe)。如果 Windows SmartScreen 弹出提示，请先确认文件来自本仓库，再选择 **更多信息 → 仍要运行**。

2. **打开，并选择语言**  
   选择 **简体中文** 或 **English**。运行过程中可以随时切换，FirstWindow 会记住你的选择。

3. **点击「一键就绪」**  
   FirstWindow 会检查电脑并准备安全的 $0 通道。只有真正需要你决定的事情才会询问：
   - 如果缺少 Hermes，只需确认一次官方安装；
   - 如果 Agnes 云端通道需要 API Key，按提示粘贴你自己的 Key；
   - 确认当前账号/Key 对**你的账号**确实是 $0。

   Agnes 官方网站目前展示 **Free API**：[agnes-ai.com](https://agnes-ai.com/)。不同账号的计费状态可能不同，因此 FirstWindow 仍会要求你亲自确认，而不会替你猜。

4. **选择项目文件夹**  
   选择允许 FirstWindow 操作的项目目录。如果只是想先体验，可以点 **试用演示项目**。

5. **描述任务，然后点击「开始」**  
   直接用普通话描述你想做什么，例如：

   > 帮我做一个简单的个人网站，并检查它能不能正常运行。

   如果任务中途被打断，再次选择同一个项目文件夹，然后点 **继续**，不用从头重来。

<!-- QUICKSTART:END -->

正常使用到这里就够了。

## 「一键就绪」实际上帮你做了什么

这些内容**不用先学会**，知道 FirstWindow 会自动处理即可：

- 检查 Hermes 是否可用；
- 需要时准备 FirstWindow 专用的 Agnes 通道；
- 阻止未知成本的自动 fallback；
- 在「开始」解锁前做一次真实就绪检查；
- 把 Agent 的工作范围固定在你选择的项目文件夹。

安装软件、输入你自己的 API Key、确认账号是否为 $0 仍然需要你明确操作。这些是安全和成本边界，不会被偷偷自动化。

## 如果 FirstWindow 要求 Agnes API Key

1. 打开 [agnes-ai.com](https://agnes-ai.com/)。
2. 选择网站里的 **Free API / Access API** 入口，需要时登录账号。
3. 在 Agnes 的账号/API 页面创建或复制 API Key。
4. 回到 FirstWindow，把 Key 粘贴到隐藏输入框。
5. 确认这个账号/Key 对你的账号是 $0，然后让 FirstWindow 完成真实就绪检查。

FirstWindow 只把这个 Key 保存到自己的隔离 Hermes 配置中。它不会从你平时的 Hermes 配置复制其他 Provider Key，不会把 Key 写入任务状态，不会打印到日志，也不会作为命令行参数传递。

## 如果 Windows 出现 SmartScreen

当前社区版 EXE 尚未签名，因此 Windows 可能显示“未知发布者”。

如果你希望进一步校验，可以从同一个 Release 下载 [SHA256SUMS.txt](https://github.com/wookzzz57-beep/first-window/releases/latest/download/SHA256SUMS.txt)，然后运行：

```powershell
Get-FileHash .\FirstWindow-Windows-x64.exe -Algorithm SHA256
Get-Content .\SHA256SUMS.txt
```

两个 SHA-256 值必须一致。

## 如果「一键就绪」没有完成

直接按照 FirstWindow 弹出的下一步处理。常见情况：

- **缺少 Hermes** — 同意官方安装，FirstWindow 会继续后面的步骤。
- **缺少 Agnes API Key** — 把自己的 Key 粘贴到隐藏输入框。
- **还没有确认 $0** — 只有在当前账号确实免费时才确认。
- **本地模型未就绪** — 高级用户可以另外配置经过验证的 Hermes Managed Local 模型。
- **真实就绪检查失败** — FirstWindow 不会在这个通道上启动任务。修复提示的问题后，再点一次「一键就绪」。

FirstWindow 默认 fail closed：无法验证安全通道时就停止，不会偷偷切换到未知收费 Provider。

## 语言切换

Windows 应用目前支持：

- **简体中文**
- **English**

右上角可以随时切换语言。选择会保存，下一次打开仍会使用上次的语言。

English guide: **[English Beginner Guide](BEGINNER.md)**

## 底层是怎么工作的

这一部分是可选内容，新手第一次使用不需要先看。

```text
FirstWindow
  └─ Hermes Agent
       ├─ Agnes API         ← 云端通道
       └─ Managed Local     ← 可选本地通道
```

FirstWindow 负责控制和验收；Hermes Agent 负责执行。Agnes API 可以作为云端 Provider。正常新手路径不需要直接使用 Agnes CLI。

### 凭据边界

在 FirstWindow 中输入的 Agnes Key 只会写入隔离的 `firstwindowzero` Hermes profile。

FirstWindow **不会**：

- 复制默认 Hermes 的 `.env`；
- 导入无关 Provider 的 Key；
- 把凭据写进 `.firstwindow/tasks/`；
- 在日志里打印 Agnes Key；
- 把 Key 作为命令行参数传递；
- Agnes 验证失败后偷偷切换其他 Provider。

删除这个隔离 profile，也会删除 FirstWindow 保存的那份 Key。

### 项目目录安全

FirstWindow 使用多层兼容保护，把 Agent 的工作目录固定到你选择的项目文件夹，包括进程工作目录、Hermes 项目目录参数、禁止恢复旧 cwd，以及 `TERMINAL_CWD`。

### 断点继续

每个任务都会把本地恢复状态保存在：

```text
.firstwindow/tasks/<task_id>/
```

里面包含任务目标、检查点、下一步、证据和执行证明。点击 **继续** 时恢复的是同一个持久化任务，而不是依赖隐藏聊天记录。

### Agent 说“完成”不等于真正完成

FirstWindow 把“Agent 执行成功”和“结果已经验收”分开：

- **AC-001** — Agent 通过已验证的执行通道完成运行。
- **AC-002** — 实际任务结果经过独立检查。

Agent 正常退出可以覆盖 AC-001，但不会自动覆盖 AC-002。

```text
Agent 执行结束
    ↓
执行通过
    ↓
独立检查结果
    ↓
VERIFIED
```

## 高级 CLI

正常 Windows 新手流程不需要使用这些命令。

```bash
firstwindow tasks --project .
firstwindow resume <task_id> --project .
firstwindow verify <task_id>
```

源码安装和更多 CLI 示例请看主 [README](../README.md)。
