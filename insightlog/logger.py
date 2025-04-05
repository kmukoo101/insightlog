"""
Combines redaction, entropy filtering, structured formatting,
multiple output sinks, and optional tamper-evident chaining.
"""

import logging
import os
from .filters import RedactionFilter, EntropyFilter
from .formatter import StructuredFormatter
from .sinks import FileSink, ConsoleSink, EncryptedAuditSink
from .utils import hash_chain_entry


class InsightLogger:
    def __init__(self, name="insightlog", config=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.prev_hash = None

        self.config = config or {}
        self.formatter = StructuredFormatter()
        self.logger.handlers.clear()

        # Filters
        if self.config.get("filters", {}).get("enable_redaction", True):
            self.logger.addFilter(RedactionFilter())

        if self.config.get("filters", {}).get("enable_entropy_filter", True):
            self.logger.addFilter(EntropyFilter(threshold=self.config.get("filters", {}).get("entropy_threshold", 4.5)))

        # Sinks
        outputs = self.config.get("outputs", ["console"])
        if "console" in outputs:
            self.logger.addHandler(ConsoleSink(self.formatter))

        if "file" in outputs:
            file_path = self.config.get("file_path", "insightlog.log")
            self.logger.addHandler(FileSink(file_path, self.formatter))

        if "encrypted_audit" in outputs:
            path = self.config.get("encrypted_audit_path", "audit.log.enc")
            password = self.config.get("audit_password", "changeme")
            self.logger.addHandler(EncryptedAuditSink(path, password))

    def log(self, level, msg, **kwargs):
        structured = self.formatter.format_structured(msg, kwargs)

        if self.config.get("audit_hash_chain", False):
            chain_hash = hash_chain_entry(structured, self.prev_hash)
            self.prev_hash = chain_hash
            structured = f"{structured} | ChainHash: {chain_hash}"

        self.logger.log(level, structured)

    def info(self, msg, **kwargs):
        self.log(logging.INFO, msg, **kwargs)

    def warning(self, msg, **kwargs):
        self.log(logging.WARNING, msg, **kwargs)

    def error(self, msg, **kwargs):
        self.log(logging.ERROR, msg, **kwargs)

    def debug(self, msg, **kwargs):
        self.log(logging.DEBUG, msg, **kwargs)

    def critical(self, msg, **kwargs):
        self.log(logging.CRITICAL, msg, **kwargs)


# Optional CLI wrapper for testing
if __name__ == "__main__":
    import argparse
    from .config import load_config

    parser = argparse.ArgumentParser()
    parser.add_argument("--message", help="Log message", required=True)
    parser.add_argument("--level", help="Log level", default="info")
    parser.add_argument("--config", help="Path to config YAML/JSON", default=None)
    args = parser.parse_args()

    config = load_config(args.config) if args.config else {}
    log = InsightLogger(config=config)

    getattr(log, args.level.lower())(args.message, user="cli-test", context="demo")
