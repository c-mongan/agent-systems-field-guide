---
id: hidden-optional-ci
status: avoid
evidence:
  - pinned-validation
---
# Hidden optional CI

A required validator silently skips when its command is absent or fails to install.

## Symptoms

- logs say “tool not found; continuing”;
- `|| true` masks a failed gate;
- `continue-on-error` is used for release checks;
- local and CI profiles claim the same coverage while running different tools;
- the release report does not list executed steps.

## Better boundary

Create explicit profiles:

- **core:** checks that are available after installing the pinned Python dependencies;
- **release:** core plus exact third-party validators.

A missing release tool must fail. Reports must say which profile ran.

## Proof required

Temporarily remove a required validator and confirm the release profile fails. The repository's CI validator also rejects known skip patterns.

**Evidence:** `pinned-validation`
