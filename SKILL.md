---
name: choose-skills
description: 在用户准备启动一个新项目、进入实现前规划阶段、询问“该用哪些 skill”、想从本地 skills 库中挑选最合适的技能组合，或明确要求先推荐 skills 再开工时，使用这个 skill。它会先检查当前机器上已安装的 Codex 和通用 skills，再输出一行可直接复制的 `@skill-a @skill-b @skill-c` 推荐列表，并给出简短理由。即使用户没有明确说“skills”，只要他在项目开工前需要一套合适的 skill 组合，也应优先使用这个 skill。
---

# Choose Skills

为用户当前要做的项目，推荐一组最合适的本地已安装 skills。

重点不是“把所有相关 skill 都列出来”，而是帮用户在开工前选出一套互补、不过度重复、能直接上手的组合。

## Workflow

1. 先理解项目需求，再推荐。
   提炼这些信息：
   - 项目类型：网站、SaaS、内容、研究、创业验证、API 集成、微信图文等
   - 技术栈：React、Next.js、静态 HTML、移动端、未知
   - 当前阶段：探索、设计、实现、审查、优化、发布前
   - 用户最在意的结果：速度、视觉质量、验证想法、增长、合规、找 API

2. 先读取本地 skills 清单，不要凭记忆猜。
   运行这个 skill 自带的脚本，并把路径解析到当前 skill 目录，而不是项目工作目录。可用命令示意：

   ```bash
   python3 <this-skill-dir>/scripts/catalog_local_skills.py
   ```

   这个脚本会扫描：
   - `~/.codex/skills`
   - `~/.agents/skills`

   如果脚本失败，再手动查看这两个目录下的 `SKILL.md`。

3. 从本地技能库里筛选候选项。
   选择时遵循这些原则：
   - 优先推荐与当前需求直接匹配的 skill
   - 优先推荐互补 skill，不要推荐一堆做同一件事的 skill
   - 默认推荐 `2-5` 个 skill；只有复杂项目才推荐到 `6` 个
   - 相同或近似能力只保留一个主选，除非用户明确要比较方案
   - 如果 `codex` 来源和 `agents` 来源有同名 skill，优先使用 `codex`
   - 跳过明显的备份目录、重复版本或历史遗留项

4. 生成结果时，先给可复制的调用串，再给理由。

## Selection Heuristics

把 skill 分成三类来配：

- 主技能：最直接解决当前任务的 skill
- 辅助技能：提升结果质量或补足短板
- 守门技能：负责审查、规范、最佳实践

常见映射：

- Web / Landing Page / Dashboard / UI 实现
  优先考虑：`frontend-design`
  视情况补充：`impeccable`、`make-interfaces-feel-better`、`design-and-refine`、`superdesign`
  如果是 React / Next.js：可补 `vercel-react-best-practices`
  如果用户要审查 UI / UX / 可访问性：可补 `web-design-guidelines`

- UI 方案探索而不是直接落代码
  优先考虑：`superdesign` 或 `design-and-refine`

- 只做界面最后一轮精修
  优先考虑：`impeccable` 或 `make-interfaces-feel-better`

- 微信公众号 / 图文生成 / 小绿书 / Markdown 转微信
  优先考虑：`md2wechat`

- API 调研与选型
  优先考虑：`public-apis`

- 网站像素级复刻 / 仿站
  优先考虑：`clone-website`

- 近 30 天热点、舆情、趋势、内容研究
  优先考虑：`last30days`

- 创业方向、想法验证、MVP、增长、定价
  依阶段组合：
  - 起点模糊：`find-community`
  - 验证想法：`validate-idea`
  - 手工交付版：`processize`
  - 做最小产品：`mvp`
  - 定价：`pricing`
  - 找前 100 个客户：`first-customers`
  - 内容增长：`marketing-plan`
  - 扩张决策：`grow-sustainably`
  - 全局复盘：`minimalist-review`

- 用户想找更多 skill，而不是立刻开工
  优先考虑：`find-skills` 或 `awesome-claude-skills`

- 用户想创建、修改、优化 skill
  优先考虑：`skill-creator`

## Avoid Redundancy

默认不要同时推荐这些组合，除非用户明确说要多方案并行：

- `frontend-design` + `superdesign` + `design-and-refine`
- `impeccable` + `make-interfaces-feel-better`
- `find-skills` + `awesome-claude-skills`

如果确实要一起推荐，必须解释分工差异。

## Output Format

始终先输出一行只包含 skill 调用列表，格式如下：

```text
@skill-a @skill-b @skill-c
```

规则：
- 使用本地真实安装的 skill 名称
- 不要写路径
- 不要加逗号
- 不要在第一行混入解释文字
- 如果只推荐一个 skill，就只输出一个 `@name`

第一行之后，再追加简短说明：

```text
@skill-a @skill-b @skill-c

Why these
- skill-a: 一句话说明它为什么是主技能
- skill-b: 一句话说明它补什么
- skill-c: 一句话说明它负责什么

Optional swaps
- 如果用户更偏向 X，可把 @skill-b 换成 @other-skill
```

`Optional swaps` 只有在确实存在接近但不同路线时才写；否则省略。

## Fallback Behavior

如果本地没有强匹配 skill，不要硬凑。
此时输出：

```text
@find-skills

Why these
- 当前本地 skill 库里没有足够贴合的技能，先用它补搜更合适的 skill。
```

不要把 `@choose-skills` 推荐回结果里；它负责做选择，不负责成为最终推荐对象。

## Examples

**Example 1**

用户：
“我准备做一个 Next.js 的 SaaS 官网，想先把设计做高级一点，再开始写页面。”

输出：

```text
@frontend-design @vercel-react-best-practices @impeccable
```

**Example 2**

用户：
“我有个创业想法，想先判断值不值得做，然后看看怎么快速做 MVP。”

输出：

```text
@validate-idea @processize @mvp
```

**Example 3**

用户：
“我要把一篇 Markdown 文章转成微信公众号图文，并且看看封面怎么做。”

输出：

```text
@md2wechat
```

## Final Reminder

你的任务是帮助用户在开工前“减负”，不是堆技能名。

宁可给一套精炼、互补、能立刻上手的 skill 组合，也不要给一长串看起来都沾边、但实际上让用户更难选的列表。
