"""
InsightLog Utilities

Includes:
- High-entropy string detection
- Known secret keyword detection
- Hash chaining for tamper-evident audit logs
"""

import math
import re
import hashlib
import os
import json
import string


SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key ID
    re.compile(r"(?i)secret[_-]?key\s*[=:]\s*[a-z0-9/+=]{16,}"),
    re.compile(r"(?i)api[_-]?key\s*[=:]\s*[a-z0-9/+=]{16,}"),
    re.compile(r"(?i)password\s*[=:]\s*\S+"),
    re.compile(r"(?i)authorization\s*[=:]\s*Bearer\s+\S+"),
]


def shannon_entropy(data):
    """
    Calculate Shannon entropy of a string to measure randomness.
    """
    if not data:
        return 0
    entropy = 0
    length = len(data)
    symbols = set(data)
    for symbol in symbols:
        p = data.count(symbol) / length
        entropy -= p * math.log2(p)
    return entropy


def contains_high_entropy(data, threshold=4.5):
    """
    Return True if any word exceeds the entropy threshold.
    """
    tokens = data.split()
    for token in tokens:
        if len(token) >= 8 and shannon_entropy(token) > threshold:
            return True
    return False


def contains_secret_patterns(data):
    """
    Return True if any known secret pattern is matched.
    """
    for pattern in SECRET_PATTERNS:
        if pattern.search(data):
            return True
    return False


def hash_chain_entry(log_line, prev_hash=None):
    """
    Create a chained hash of a log line + previous hash.
    """
    combined = (prev_hash or "") + log_line
    return hashlib.sha256(combined.encode()).hexdigest()


def is_printable_json(obj):
    """
    Check if an object is printable JSON (no binary, no deeply nested).
    """
    try:
        s = json.dumps(obj)
        return all(c in string.printable for c in s)
    except Exception:
        return False
