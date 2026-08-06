# Argus

> 面向长周期任务的自主科研与工程运行时，让工作不再受限于一次模型调用。

[官方网站](https://argusbot.cn) · [演示视频](https://www.youtube.com/watch?v=i8Qy9HCboQE) · [技术报告](technical_report/argus-technical-report.pdf) · [English](README.md)

## Argus 是什么？

Argus 将开放目标转化为可持续、可审查的工作流。它跨 session 保存项目状态，并协调四个相互独立的角色：

| 角色 | 职责 |
|---|---|
| **Manager** | 理解 operator 意图、选择工作流并控制阶段迁移。 |
| **Planner** | 选择下一项高价值任务并定义证据要求。 |
| **Engineer** | 实现代码、开展调研和实验并生成产物。 |
| **Reviewer** | 独立检查正确性、证据、局限和完成状态。 |

运行时会持久化任务、检查点、决策、可复用 Skill 与审查证据。项目可以停止、恢复、跨进程升级，并从最近一次已验证状态继续运行。

Argus 支持 GitHub Copilot CLI、OpenAI Codex CLI、Claude Code、OpenCode 与 Pi。

## 安装

### 环境要求

- Python 3.11+
- Node.js 22+
- 至少一个已按官方方法安装并完成鉴权的 agent CLI

### 1. 克隆并安装

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2. 配置后端

选择你已经在使用的后端：

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

可将 `copilot` 替换为 `codex`、`claude`、`opencode` 或 `pi`。启动 Argus 前，请先使用对应 CLI 的官方登录流程完成鉴权。

### 3. 启动

```bash
argus
```

常用检查：

```bash
argus --doctor
argus --status
```

## 更新

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

启动器会识别过期的本地 WebAPI 与 daemon，并在受控任务边界完成替换。
