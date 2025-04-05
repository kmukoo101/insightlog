"""
InsightLog
==========

This is a secure, context-aware, advanced Python logging package
built for security analysts, DevOps engineers, and incident responders.
It supports sensitive data redaction, entropy-based leak detection,
categorized outputs, encrypted audit trails, and multiple log sinks.

"""

from .logger import InsightLogger
from .config import load_config
from .filters import RedactionFilter, EntropyFilter
from .sinks import FileSink, ConsoleSink, EncryptedAuditSink
from .formatter import StructuredFormatter

__all__ = [
    "InsightLogger",
    "load_config",
    "RedactionFilter",
    "EntropyFilter",
    "FileSink",
    "ConsoleSink",
    "EncryptedAuditSink",
    "StructuredFormatter"
]
