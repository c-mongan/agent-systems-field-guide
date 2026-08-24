# Verification reports

Run the local, network-free profile after installing the pinned Python tools:

```bash
python scripts/verify.py --profile core --report-dir reports
```

CI runs the stricter release profile. It also requires the exact Ruff, Mypy, and `agnix` versions configured in the repository:

```bash
python scripts/verify.py --profile release --report-dir reports/ci
```

A missing release tool is a failure. Live provider benchmarks are separate because they require credentials and exact model identifiers.
