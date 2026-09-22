# gruntwork-tap

Gruntwork infrastructure-as-code as grid vocabulary: v0 carries one outer node, the Gruntwork deployment (the account factory and infrastructure-live estate it manages), so a design can place it before anything is collected.

## What this plugin owns

One type in v0: `gruntwork__gruntwork_deployment` — a Gruntwork deployment: the Gruntwork-managed estate (account factory, infrastructure-live repository and pipelines) that provisions and governs a set of cloud accounts. A design can place it before any access exists; everything inside it is later vocabulary.

## Read first

`specs/spec-gruntwork-v0.md` — this is a thin v0 that puts the piece on the board; the full spec interview runs when the plugin grows.

## Stand it up

From a TAP core checkout:

```bash
scripts/spawn-session.sh <label> cli --from 'git+https://github.com/unified-systems-com/gruntwork-tap@<rev>#ci' --dev-plugins gruntwork
```
