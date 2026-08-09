# Research Workflow Skill for Pi / Hermes

> 从 Argus 架构获得灵感，为 Pi 和 Hermes 用户打造的纯 Skill 实现

## 背景

我是 Pi 和 Hermes 的用户。在使用 Argus 的过程中遇到了一些安装和运行上的问题（Python 环境依赖、后端配置、版本兼容等），于是萌生了一个想法：能不能把 Argus 这种多角色研究 Agent 的核心思想，直接写成 Pi 的一个 Skill？

结果比我预想的还要好。

## 这是什么

一个**纯 Markdown Skill 文件**（`SKILL.md`），放入 Pi/Hermes 的 `skills` 目录即可使用。不需要安装任何 Python 包，不需要配置后端，不需要管理进程——Skill 本身就是 Agent。

### 核心设计

```
User Request
  │
  ├─ [Planner] ──────────── 任务拆解，定义深度目标
  ├─ [Researcher] ───────── 每个任务前收集外部信息（NEW）
  ├─ [Engineer R1] ──────── 基线执行
  │     │
  ├─ [Reviewer-Challenger] ─ 验证 + 挑战："在 X 上再深入一层"（UPGRADED）
  │     │
  ├─ [Engineer R2] ──────── 深度探索
  │     │
  ├─ [Reviewer-Challenger] ─ 验证 + 挑战："外部来源怎么说？"
  │     │
  ├─ [Engineer R3+] ─────── 外部知识富化（NEW）
  │     │
  ├─ [Cross-Task Reflector] ─ 跨任务学习提取（NEW）
  │     │
  ├─ [Planner Replan Gate] ─ 根据新知识调整剩余计划（NEW）
  │
  └─ [Synthesis] ────────── 编译、关联、总结
```

### 与 Argus 的核心区别

| | Argus | Research Workflow Skill |
|---|---|---|
| **运行方式** | Python 独立进程，多后端 | Pi/Hermes Skill，零安装 |
| **配置** | Python venv + 后端认证 | 放入 skills 目录即可 |
| **Reviewer** | 验证 + 通过/修改 | 验证 + **挑战** + 深度门控 |
| **信息获取** | Engineer 执行中使用工具 | Researcher 阶段**在执行前**搜索 |
| **跨任务学习** | 无 | Cross-Task Reflector 提取 + 影响后续计划 |
| **深度保证** | 取决于模型 | R1→R2→R3 强制多轮深化 |
| **迭代速度** | Python 代码修改 | 直接改 Prompt，分钟级迭代 |

### 为什么效果好

1. **零依赖安装**：一个 Markdown 文件，不需要 pip install，不需要 Node.js 版本匹配
2. **Prompt-native**：大模型"理解" Skill 比理解 Python 代码更自然，遵循度更高
3. **极速迭代**：改 prompt 就改行为，不需要跑测试、等 CI
4. **信息密度高**：Researcher 角色在每次执行前强制搜索外部信息，Reviewer-Challenger 会追问"有没有外部数据支持"
5. **深度门控**：R1 基线 → R2 深化 → R3 外部富化，Reviewer 不在第一轮就放行

### 使用方式

```bash
# 安装到 Pi
cp SKILL.md ~/.pi/agent/skills/research-workflow/

# 安装到 Hermes
cp SKILL.md ~/.hermes/skills/research-workflow/
```

然后在对话中说 "研究一下..."、"分析这个方向..."、"写一篇 survey..."，Skill 自动激活。

## 致谢

灵感来自 [Argus](https://github.com/lbx154/Argus) 的多角色协作架构（Manager → Planner → Engineer ⇄ Reviewer）。虽然这个 Skill 已经和 Argus 关系不大了，但 Argus 的设计思想——**把执行和评审分开、多角色各司其职**——是这一切的起点。

感谢 lbx154 和 Argus 团队的工作！
