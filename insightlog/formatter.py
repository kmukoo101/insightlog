"""
Log Formatters for InsightLog

Provides:
- StructuredFormatter: JSON-style structured formatter with color support for console
"""

import logging
import json
import sys
from datetime import datetime

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False


class StructuredFormatter(logging.Formatter):
    """
    A structured log formatter that outputs logs as JSON or plaintext.

    Args:
        json_output (bool): If True, outputs logs in JSON format.
        color (bool): If True, applies color to console output.
    """

    def __init__(self, json_output=False, color=False):
        super().__init__()
        self.json_output = json_output
        self.color = color and COLOR_SUPPORT

    def format(self, record):
        record_dict = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extras if available
        if hasattr(record, "tag"):
            record_dict["tag"] = record.tag
        if hasattr(record, "event_id"):
            record_dict["event_id"] = record.event_id

        if self.json_output:
            return json.dumps(record_dict)

        msg = f"[{record_dict['timestamp']}] [{record_dict['level']}] [{record_dict['logger']}] {record_dict['message']}"

        if self.color:
            msg = self._apply_color(record.levelname, msg)

        return msg

    def _apply_color(self, level, msg):
        """Apply ANSI color codes based on log level."""
        if level == "DEBUG":
            return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"
        elif level == "INFO":
            return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"
        elif level == "WARNING":
            return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
        elif level in ("ERROR", "CRITICAL"):
            return f"{Fore.RED}{msg}{Style.RESET_ALL}"
        return msg
