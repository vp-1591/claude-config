---
name: planner
description: >-
  Write a plan than check that it's following best practices
disable-model-invocation: true
argument-hint: [goal]
---
Write a plan for the following query:
$ARGUMENTS
After you write a plan, review it for significant YAGNI, DRY, KISS, SoC and SOLID violations and flag them to user. Do not update plan before user decides whether these violations should be fixed and how they should be fixed.
