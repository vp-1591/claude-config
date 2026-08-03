---
name: planner
description: >-
  Write a plan, then review it for YAGNI/DRY/KISS/SoC/SOLID violations before implementation
disable-model-invocation: true
argument-hint: [goal]
---
1. Write a plan for: $ARGUMENTS
2. Review the plan for significant YAGNI, DRY, KISS, SoC, and SOLID violations. Report any
   found directly in your response — do not silently fix them.
3. Write a mermaid diagram of the affected data/control flow to
   tmp/diagram-<kebab-case-goal-summary>.md and present it alongside the plan and any
   flagged violations.
4. Wait for the user to decide whether and how to address each flagged violation.
5. If the user requests changes, update both the plan and the diagram to match before
   exiting plan mode.