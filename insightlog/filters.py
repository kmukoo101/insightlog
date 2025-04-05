"""
Filters for Redacting Secrets and High-Entropy Strings

These filters can be attached to loggers to automatically clean sensitive data
before it is logged.

- RedactionFilter: removes secrets based on regex patterns
- EntropyFilter: removes secrets based on entropy threshold
"""

import re
import logging
import math


def shannon_entropy(data):
    """
    Calculate the Shannon entropy of a string.

    Args:
        data (str): The input string

    Returns:
        float: entropy score
    """
    if not data:
        return 0.0
    entropy = 0
    length = len(data)
    for x in set(data):
        p_x = float(data.count(x)) / length
        entropy += - p_x * math.log2(p_x)
    return entropy


class RedactionFilter(logging.Filter):
    """
    A logging filter that redacts sensitive data based on regex patterns.

    Args:
        patterns (list): List of regex strings
        replacement (str): Redacted placeholder text
    """

    def __init__(self, patterns=None, replacement="***REDACTED***"):
        super().__init__()
        self.patterns = [re.compile(p) for p in patterns or []]
        self.replacement = replacement

    def filter(self, record):
        if not isinstance(record.msg, str):
            return True

        for pattern in self.patterns:
            record.msg = pattern.sub(self.replacement, record.msg)

        return True


class EntropyFilter(logging.Filter):
    """
    A logging filter that redacts high-entropy strings (e.g., API keys).

    Args:
        threshold (float): Entropy threshold for redaction
        min_length (int): Minimum length of token to evaluate
    """

    def __init__(self, threshold=4.2, min_length=8):
        super().__init__()
        self.threshold = threshold
        self.min_length = min_length

    def filter(self, record):
        if not isinstance(record.msg, str):
            return True

        tokens = record.msg.split()
        cleaned = []

        for token in tokens:
            if len(token) >= self.min_length and shannon_entropy(token) > self.threshold:
                cleaned.append("***ENTROPY_REDACTED***")
            else:
                cleaned.append(token)

        record.msg = " ".join(cleaned)
        return True
