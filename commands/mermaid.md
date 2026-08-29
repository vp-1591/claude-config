---
name: mermaid
description: >-
  Create mermaid diagram.
disable-model-invocation: true
argument-hint: [target]
---

Create mermaid of $ARGUMENTS
Save it wrapped in a ```mermaid block to tmp/diagram-[slug].md

Validate the generated syntax:
mmdc -i tmp/diagram-[slug].md -o - > /dev/null