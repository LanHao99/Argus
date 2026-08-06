<div align="center">
  <h1>ARGUS</h1>
  <p><strong>让自主科研真正持续运行。</strong></p>
  <p>面向长期 Agent 的持久运行时：能够规划、执行、验证、暂停，并在一次模型调用之后继续推进。</p>
  <p>
    <a href="https://argusbot.cn"><strong>官方网站</strong></a>
    &nbsp;·&nbsp;
    <a href="https://www.youtube.com/watch?v=i8Qy9HCboQE"><strong>演示视频</strong></a>
    &nbsp;·&nbsp;
    <a href="https://arxiv.org/pdf/2608.05144"><strong>技术报告 · arXiv:2608.05144</strong></a>
    &nbsp;·&nbsp;
    <a href="README.md"><strong>English</strong></a>
  </p>
  <p>
    <code>PREVIEW · v0.1.1</code>
    &nbsp;
    <code>正式开源版 · ON THE WAY</code>
  </p>
</div>

---

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>持久，而不是一次性</h3>
      任务、检查点、决策、Skill 与审查证据会跨 session 和进程升级持续保存。
    </td>
    <td width="50%" valign="top">
      <h3>默认独立审查</h3>
      执行与验证相互分离；每个正常回合都以独立 Reviewer 的判断结束。
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Agent 原生工作方式</h3>
      角色直接使用真实文件、工具、终端、实验和产物，而不是被限制在封闭的流程编辑器中。
    </td>
    <td width="50%" valign="top">
      <h3>为扩展而设计</h3>
      通过角色规则、工具、阶段、证据标准和 Vertical，把运行时改造成真正适合你的系统。
    </td>
  </tr>
</table>

## 一个运行时，四种权威

<table>
  <tr>
    <td width="25%" valign="top">
      <strong>01 · MANAGER</strong><br><sub>控制</sub><br><br>
      理解 operator 意图、选择工作流，并独占阶段迁移权。
    </td>
    <td width="25%" valign="top">
      <strong>02 · PLANNER</strong><br><sub>方向</sub><br><br>
      选择下一项高价值任务，并定义它必须产出的证据。
    </td>
    <td width="25%" valign="top">
      <strong>03 · ENGINEER</strong><br><sub>执行</sub><br><br>
      实现代码、开展调研、运行实验，并生成可检查的产物。
    </td>
    <td width="25%" valign="top">
      <strong>04 · REVIEWER</strong><br><sub>验证</sub><br><br>
      独立检查正确性、证据、局限和完成状态。
    </td>
  </tr>
</table>

Argus 通过持久项目状态连接这四种权威。项目可以停止、恢复、跨运行时替换，并从最近一次已验证位置继续推进。

**原生 Agent Backend** &nbsp; `GitHub Copilot CLI` · `Pi` · `OpenAI Codex CLI` · `Claude Code` · `OpenCode`

---

## 三步开始

### 1 · 安装

**环境要求：** Python 3.11+、Node.js 22+，以及至少一个已完成登录鉴权的 Agent CLI。

```bash
git clone https://github.com/lbx154/Argus.git
cd Argus

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

### 2 · 连接后端

```bash
argus --setup --non-interactive \
  --backend copilot \
  --accept-house-rules
```

`--backend` 可使用 `copilot`、`pi`、`codex`、`claude` 或 `opencode`。

### 3 · 启动

```bash
argus
```

```bash
argus --doctor   # 检查安装与后端
argus --status   # 查看当前运行状态
```

---

## 选择你的交互界面

### Terminal Cockpit

```bash
argus
```

终端 Cockpit 是与 Manager 对话、跟踪实时工作、检查状态和恢复项目最快的入口。

### Web UI

启动 Argus，并在默认浏览器中打开 Web UI：

```bash
argus --web
```

默认地址：[http://127.0.0.1:8799](http://127.0.0.1:8799)

```bash
argus --web --no-open    # 只启动，不打开浏览器
argus --web --port 8800  # 使用其他端口
```

#### 通过 SSH 使用远程服务器（推荐）

在服务器上：

```bash
argus --web --no-open
```

在自己的电脑上：

```bash
ssh -L 8799:127.0.0.1:8799 user@server
```

然后在本机打开 [http://127.0.0.1:8799](http://127.0.0.1:8799)。

<details>
<summary><strong>直接通过局域网访问</strong></summary>

<br>

直接访问局域网时，必须使用 Bearer Token 保护服务：

```bash
export ARGUS_SKILL_WEB_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
printf '%s\n' "$ARGUS_SKILL_WEB_TOKEN"
argus --web --host 0.0.0.0 --port 8799 --no-open
```

从其他设备打开下面的地址，并替换服务器 IP 与 Token：

```text
http://SERVER_IP:8799/?token=YOUR_TOKEN
```

禁止在未设置 `ARGUS_SKILL_WEB_TOKEN` 时将服务暴露到 `0.0.0.0`。

</details>

---

## 设计你自己的 Argus

Argus 的设计目标不是“只能配置”，而是“可以被你改变”。

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>重塑整个运行时</h3>
      调整角色 Prompt、工作流边界、审查策略、工具与运行约定，让完整闭环真正符合你的工作方式。
    </td>
    <td width="50%" valign="top">
      <h3>创建自己的 Vertical</h3>
      为你的领域加入专属阶段、Skill、数据集、工具、证据要求、评测方法与完成标准。
    </td>
  </tr>
</table>

如果你是 Agent 的狂热爱好者，我们推荐你在本地运行并持续改造 Argus，把它变成真正服务于自己伟大领域的运行时。用测试固定你重视的行为，连接已有基础设施，让规划和审查遵循你的领域标准，而不是一套通用流程。

### 让其他 Agent 成为外层入口

你可以通过 GitHub Copilot、Pi、Codex、Claude Code、OpenCode、OpenClaw 或 Hermes 调用 Argus、检查状态、操作本地 CLI 或 Web/API，并继续迭代自己的部署。

- **Argus 原生 Backend：** GitHub Copilot CLI、Pi、Codex CLI、Claude Code、OpenCode
- **外层 Agent：** OpenClaw、Hermes，或任何能够使用 Shell / HTTP API 的 Agent

常用入口：

```bash
argus --doctor
argus --status
argus --web --no-open
```

---

## 更新

```bash
cd Argus
git pull --ff-only
.venv/bin/python -m pip install -e .
.venv/bin/argus
```

Argus 会识别过期的本地 WebAPI 与 daemon，并在受控任务边界完成替换。
