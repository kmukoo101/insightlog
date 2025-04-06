# InsightLog (InsightLog101)

This is a secure, context-aware Python logging utility that provides advanced features for redacting sensitive data, exporting logs to encrypted formats, filtering by severity and tags, and generating tamper-evident audit trails.

---

## Features

- Redacts secrets using pattern and entropy-based detection
- Dual output: human-readable console + structured JSON logs
- Categorization and filtering by severity and tags
- File, console, and encrypted audit log support
- Tamper-evident hash-chained logs (optional)
- Configurable via YAML, JSON, or environment variables
- Supports CLI mode and decorator-based tracing

---

## Installation

```bash
pip install git+https://github.com/kmukoo101/insightlog.git
```

Or clone the repo and use:

```bash
pip install .
```

---

## Basic Usage

```python
from insightlog import InsightLogger

logger = InsightLogger(name="myapp")
logger.info("User logged in", extra={"user_id": "123"})
logger.warning("Suspicious input", extra={"input": "password=secret123"})
```

---

## Config

You can load settings from `config.yml`, JSON, or environment variables.

Example `config.yml`:

```yaml
level: DEBUG
console: true
file: logs/app.log
redact_patterns:
  - password=.*?
  - secret_key=\w+
```

```python
from insightlog import load_config
load_config("config.yml")
```

---

## CLI Support (Optional)

This tool provides a basic CLI entry point for structured logging, useful in shell scripts or quick diagnostics.

```bash
python -m insightlog --message "System check complete" --level INFO --tag healthcheck
```
