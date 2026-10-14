# FlowBeast Git Workflow Rules

> Git conventions and best practices

## Git Philosophy

- Small commits
- Clear history
- Observable evolution

## Commit Style

Prefer conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Examples:
- `feat: add fp3 retriever ranking pipeline`
- `fix: resolve docker env loading issue`
- `refactor: simplify agent orchestration`

## Branching

Prefer short-lived branches.

Avoid:
- Massive long-running divergence
- Huge mixed-purpose commits

## AI-Generated Commits

AI-generated changes must:
- Be reviewed
- Preserve architecture consistency
- Avoid broad unrelated modifications

## Hooks

Hooks should:
- Improve quality
- Remain fast
- Avoid blocking iteration unnecessarily

## Repository Hygiene

Keep:
- Clear structure
- Predictable naming
- Minimal dead code

Avoid:
- Random experiments on main branch
- Large unrelated rewrites
