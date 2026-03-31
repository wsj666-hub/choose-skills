# choose-skills

`choose-skills` is a Codex-oriented skill that recommends the best local skill stack before you start a project.

它的目标很简单：在你真正开工前，先根据你的需求，从你本机已经安装的 skills 里挑出最合适的一组，并输出一行可直接复制的调用列表：

```text
@skill-a @skill-b @skill-c
```

Instead of dumping every vaguely related skill, it tries to recommend a compact, complementary set that helps you start fast.

## Quick Install

### Fastest option

Install globally from GitHub:

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --yes --global
```

### Install only this skill by name

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --skill choose-skills --yes --global
```

### Install to Codex only

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --skill choose-skills --agent Codex --yes --global
```

### Preview before installing

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --list
```

After installation, restart Codex or open a new session if the skill does not appear immediately.

## What It Does

- Scans your local skill library before recommending anything
- Reads both `~/.codex/skills` and `~/.agents/skills`
- Prefers Codex-native skills over duplicate universal skills when both exist
- Recommends a small set of complementary skills instead of a long, noisy list
- Starts the answer with an `@skill @skill` line you can copy immediately
- Adds short reasoning and optional swaps when helpful

## When To Use It

Use `choose-skills` when you are about to start a project and want help selecting the right skill stack first.

Typical use cases:

- “I’m starting a new Next.js landing page. Which skills should I use first?”
- “I want to build a WeChat article workflow. Recommend the right skills before we begin.”
- “I have a startup idea and want the best skills for validation and MVP planning.”
- “I installed too many skills. Help me choose the right ones for this task.”

## Output Format

The first line is always a compact invocation list:

```text
@frontend-design @vercel-react-best-practices @impeccable
```

Then it can optionally add short explanations:

```text
@frontend-design @vercel-react-best-practices @impeccable

Why these
- frontend-design: primary UI implementation and visual direction
- vercel-react-best-practices: React / Next.js performance and architecture guardrails
- impeccable: final interface polish and refinement
```

## How It Works

`choose-skills` follows a lightweight selection flow:

1. Understand the project type, stage, stack, and success criteria.
2. Inspect the local skill inventory using the bundled catalog script.
3. Filter out redundant or overlapping skills.
4. Recommend a small, high-signal set of skills.
5. Return the result in `@skill-name` format first, then add short rationale.

It is intentionally conservative. If there is no strong local match, it falls back to discovery-oriented skills such as `find-skills`.

## Skill Selection Philosophy

This skill is opinionated about two things:

- Fewer, better recommendations beat exhaustive lists.
- Complementary stacks beat redundant stacks.

For example, it will usually avoid recommending several near-duplicate design skills together unless there is a strong reason to compare multiple approaches.

## Local Skill Catalog

The bundled script:

```bash
python3 scripts/catalog_local_skills.py
```

produces a JSON catalog of locally available skills, including:

- `name`
- `description`
- `source`
- `path`

This makes the recommendations grounded in what is actually installed on your machine.

## Installation

### Recommended: use Skills CLI

If you use the open skills ecosystem, the easiest install path is:

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --skill choose-skills --yes --global
```

If you want it available specifically for Codex:

```bash
npx skills add https://github.com/wsj666-hub/choose-skills --skill choose-skills --agent Codex --yes --global
```

### Manual install for Codex

You can also copy this folder into your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R choose-skills ~/.codex/skills/choose-skills
```

Then restart Codex or start a new session.

## Usage Examples

### Example 1: Web Project

Prompt:

```text
I’m about to start a Next.js SaaS landing page. I want strong visual design and good implementation quality. Recommend the right skills first.
```

Possible result:

```text
@frontend-design @vercel-react-best-practices @impeccable
```

### Example 2: Startup Validation

Prompt:

```text
I have a business idea and want to validate it before building anything. Then I want to shape an MVP. Recommend the best skills first.
```

Possible result:

```text
@validate-idea @processize @mvp
```

### Example 3: WeChat Publishing

Prompt:

```text
I want to turn a Markdown draft into a WeChat article and think through the cover and layout. Recommend the right skills first.
```

Possible result:

```text
@md2wechat
```

## Repository Structure

```text
choose-skills/
├── README.md
├── SKILL.md
├── evals/
│   └── evals.json
└── scripts/
    └── catalog_local_skills.py
```

## Development Notes

- `SKILL.md` contains the trigger description and runtime instructions.
- `scripts/catalog_local_skills.py` catalogs installed local skills.
- `evals/evals.json` contains starter test prompts for future evaluation loops.

## Limitations

- Recommendations are only as good as the skills currently installed locally.
- It is designed for pre-project selection, not for discovering the entire public skill ecosystem.
- It returns recommendations in `@skill-name` format because that is the requested output convention, even if different environments invoke skills differently.

## Roadmap

- Better grouping of overlapping design skills
- Optional domain presets such as “web build”, “startup validation”, “content pipeline”
- More eval prompts for ambiguous edge cases

## License

MIT. See [LICENSE](./LICENSE).
