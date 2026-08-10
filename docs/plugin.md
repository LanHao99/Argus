# Argus Plugin

## 一键安装

Codex：

```bash
curl -fsSL https://raw.githubusercontent.com/lbx154/Argus/main/plugins/argus/install.sh | sh -s -- codex
```

Claude Code：

```bash
curl -fsSL https://raw.githubusercontent.com/lbx154/Argus/main/plugins/argus/install.sh | sh -s -- claude
```

两个都安装：

```bash
curl -fsSL https://raw.githubusercontent.com/lbx154/Argus/main/plugins/argus/install.sh | sh -s -- all
```

## 使用

直接告诉 Codex 或 Claude Code：

- “用 Argus 执行这个项目。”
- “查看 Argus 项目状态。”
- “用 `target-disease-research` 研究 EGFR 与肺癌。”

医学能力是 Argus 内置的 `medical` vertical，不提供诊断或治疗建议。
