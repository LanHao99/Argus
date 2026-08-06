<div align="center">

# ARGUS

### 面向自主科研与工程的持久智能运行时

把开放目标变成可规划、可执行、可审查、可暂停并继续的长期工作流。

[官方网站](https://argusbot.cn) · [演示视频](https://www.youtube.com/watch?v=i8Qy9HCboQE) · [技术报告](technical_report/argus-technical-report.pdf) · [English](README.md)

`Manager` → `Planner` → `Engineer` ⇄ `Reviewer`

</div>

---

## ✦ 一个目标，四个角色，持续推进

Argus 围绕持久项目状态，协调四个相互独立、由模型驱动的角色：

| 角色 | 负责内容 |
|---|---|
| 🧭 **Manager** | 理解 operator 意图、选择工作流并控制阶段迁移 |
| 🗺️ **Planner** | 选择下一项高价值任务并定义证据要求 |
| 🛠️ **Engineer** | 实现代码、开展调研和实验并生成产物 |
| 🔎 **Reviewer** | 独立检查正确性、证据、局限和完成状态 |

```text
operator 意图
      │
      ▼
  Manager ──► Planner ──► Engineer ──► Reviewer
      ▲                         │           │
      └──── 持久状态 ◄─────────┴───────────┘
```

任务、检查点、决策、可复用 Skill 与审查证据都会跨 session 保存。项目可以停止、恢复、跨进程升级，并从最近一次已验证状态继续运行。

**支持的 Agent CLI：** GitHub Copilot CLI · OpenAI Codex CLI · Claude Code · OpenCode · Pi

---

## ⚡ 快速开始

### 环境要求

- Python 3.11+
- Node.js 22+
- 至少一个已按官方方式安装并完成登录鉴权的 Agent CLI

### 1. 安装

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2. 连接后端

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

可根据需要将 `copilot` 替换为 `codex`、`claude`、`opencode` 或 `pi`。

### 3. 启动终端 Cockpit

```bash
argus
```

常用检查：

```bash
argus --doctor
argus --status
```

---

## ◉ Web UI

### 本机桌面环境

启动 API 与 Web UI，并自动打开默认浏览器：

```bash
argus --web
```

默认地址为 [http://127.0.0.1:8799](http://127.0.0.1:8799)。

如果只想启动服务、不自动打开浏览器：

```bash
argus --web --no-open
```

需要更换端口时：

```bash
argus --web --port 8800
```

### 通过 SSH 使用远程服务器（推荐）

先在服务器上启动，并保持只监听 localhost：

```bash
argus --web --no-open
```

然后在自己的电脑上建立端口转发：

```bash
ssh -L 8799:127.0.0.1:8799 user@server
```

最后在本机打开 [http://127.0.0.1:8799](http://127.0.0.1:8799)。

<details>
<summary><strong>直接通过局域网访问</strong></summary>

直接监听局域网地址时，必须配置 Bearer Token：

```bash
export ARGUS_SKILL_WEB_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
printf '%s\n' "$ARGUS_SKILL_WEB_TOKEN"
argus --web --host 0.0.0.0 --port 8799 --no-open
```

在其他设备上打开下面的地址，并替换服务器 IP 与 Token：

```text
http://SERVER_IP:8799/?token=YOUR_TOKEN
```

禁止在未设置 `ARGUS_SKILL_WEB_TOKEN` 时将服务暴露到 `0.0.0.0`。

</details>

---

## ↻ 更新

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

启动器会识别过期的本地 WebAPI 与 daemon，并在受控任务边界完成替换。
