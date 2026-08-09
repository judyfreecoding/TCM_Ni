# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

倪海厦讲中医 — 基于 VitePress 构建的中医学习平台，内容为中文（zh-CN）。将倪海厦讲授的中医经典重新组织为五个核心版块，并在黄帝内经部分引入了一套创新的**系统工程与中医类比理论**（DP/EP 概念、对称映射能量正相关理论、人体故障熔断与恢复逻辑）。

## 常用命令

```bash
npm run docs:dev        # 启动开发服务器（热重载）
npm run docs:build      # 构建生产静态站点
npm run docs:preview    # 本地预览生产构建
```

## 技术栈与配置

- **框架**: VitePress 1.x（使用 dark 主题作为默认外观）
- **关键插件**: `vitepress-plugin-mermaid`（Mermaid 图表）、`markdown-it-mathjax3`（数学公式 `$$...$$`）
- **配置文件**: `docs/.vitepress/config.js` — 使用 `withMermaid()` 包裹配置
- **主题定制**: `docs/.vitepress/theme/` — 仅覆写了 `custom.css`（品牌色为红色系 `#c53030`，中文雅黑字体栈）
- **本地搜索**: 配置中 `search.provider: 'local'`

## 项目结构

```
docs/
├── index.md              # 首页（hero layout，5 个功能卡片）
├── guide/                # 指南/学习路径
├── acupuncture/          # 针灸大成
│   ├── meridians/        # 十二正经（lung, heart, liver, kidney, stomach, spleen, bladder, gallbladder, small_intestine, large_intestine, pericardium, triple_energizer, 12Summarize）
│   ├── extraordinary/    # 奇经八脉（ren 任脉, du 督脉, compilation 合集）
│   ├── needling/         # 针法
│   └── moxibustion/      # 灸法（ginger 隔姜灸, garlic 隔蒜灸）
├── huangdi/              # 黄帝内经
│   ├── appendix/         # **核心创新理论**（见下方）
│   ├── summary/          # 系统总体设计（阴阳、寒热、表里虚实、五大子系统）
│   ├── subdesign/        # 子系统设计（五脏）
│   ├── networkdesign/    # 网络结构设计（主干线、特定穴位）
│   ├── case/             # 常见问题（热、痛、腹中论、络病）
│   ├── rules/            # 补泻法、针刺法则
│   ├── pulse/            # 脉法基础
│   └── others/           # 其它
├── shennong/             # 神农本草经（upper/middle/lower/supplement）
├── shanghan/             # 伤寒论
├── jinkui/               # 金匮要略
└── public/               # 静态资源（穴位图片、经络图等，按脏器/经络分子目录组织）
```

## 核心独有理论：人体系统工程框架（位于 `docs/huangdi/appendix/`）

这是此项目区别于普通中医文档的关键内容——用控制系统/网络工程语言重新诠释《黄帝内经》：

| 文件 | 内容 |
|------|------|
| `outline.md` | **总纲**：系统设计、DP 寻址规则、故障处理流程（含 Mermaid 流程图）、行动能力受限故障逻辑 |
| `symmetryTheory.md` | **对称映射能量正相关理论**：$E_{a'} = f(E_a) \cdot K$ 核心公式，故障 5 阶段熔断与恢复逻辑，经络病/内科病 DP 镜像寻址规则 |
| `failure.md` | **人体故障纠错算法**：系统故障演进（拥塞→失效→熔断→保护→恢复）、内科病分析矩阵、内科病 DP 寻址经验值表 |
| `debug.md` | **调试流程**：三阶段流程图（故障产生→调试点快速寻址→宏观脉冲修复），水锤效应防止 |
| `lineProtocol.md` | **总线协议代号表**：12 条正经的系统角色定义（如 HT="CPU 动力总线"，PC="防火墙总线"） |
| `能量衰减.md` | 三大底层物理架构支撑（KCL 回路守恒、差分镜像平衡、驻波相消干涉） |

**关键术语**：
- **DP (Debug Point / 调试点)**：线路拥塞的远端根源，表现为压痛（欠压状态），是修复入口
- **EP (Error Point / 报错点)**：系统报错/疼痛位置，因 DP 拥塞导致能量降维和熔断
- **核心原则**：不可在 EP 处艾灸（回路已断开）、不可在 DP 放血（会使欠压更甚）、通过 DP 按压恢复能量→EP 自愈

## 内容组织约定

- 每个版块在其 `index.md` 中作为概述页
- 侧边栏通过 `docs/.vitepress/config.js` 中的 `themeConfig.sidebar` 集中管理，新增页面需在该文件中注册
- 图片放在 `docs/public/`，按脏器/经络分目录，Markdown 中用 `/path` 引用（如 `/stomach/1头维.png`）
- Mermaid 图表通过 ````mermaid` 代码块嵌入，数学公式用 `$$...$$`
- 自定义容器用法（在 `guide/index.md` 中有示例）：`::: info`（重要信息）、`::: tip`（治症方案）、`::: warning`（针法）、`::: danger`（特别提醒）

## 工具脚本

- `scripts/draw_body_meridians.py` — 生成人体经络前/中/后三视图概念图（`/body_meridians_concept.png`），使用 matplotlib
- `scripts/draw_system_design.py` — 从 `总体设计.docx` 的 XML 数据还原系统总体设计图（`/system_design_overview.png`），含五行配色方案。运行后输出到 `docs/public/`
