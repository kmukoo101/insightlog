"""
Log Sinks for InsightLog

Provides:
- FileSink: logs to a plaintext file
- ConsoleSink: logs to stdout with optional color
- EncryptedAuditSink: logs securely to an encrypted file (AES)
"""

import logging
import sys
from .formatter import StructuredFormatter

from cryptography.fernet import Fernet
import base64
import os

class FileSink:
    """
    Writes logs to a specified file in plaintext or JSON format.

    Args:
        path (str): Path to the log file.
        json_output (bool): If True, outputs JSON lines.
    """
    def __init__(self, path="insightlog.log", json_output=False):
        self.handler = logging.FileHandler(path)
        self.handler.setFormatter(StructuredFormatter(json_output=json_output))

    def get_handler(self):
        return self.handler


class ConsoleSink:
    """
    Writes logs to stdout (terminal).

    Args:
        json_output (bool): If True, outputs JSON lines.
        color (bool): If True, applies color (if available).
    """
    def __init__(self, json_output=False, color=True):
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setFormatter(StructuredFormatter(json_output=json_output, color=color))

    def get_handler(self):
        return self.handler


class EncryptedAuditSink:
    """
    Logs structured messages encrypted with a symmetric key using Fernet (AES 128).

    Args:
        path (str): Path to output encrypted log file.
        key (str): Base64 encoded 32-byte key. Generate with Fernet.generate_key().
    """
    def __init__(self, path="audit.log.enc", key=None):
        self.path = path
        if key is None:
            raise ValueError("Encryption key must be provided.")
        self.fernet = Fernet(key)
        self.handler = logging.StreamHandler(stream=self)
        self.handler.setFormatter(StructuredFormatter(json_output=True))

    def write(self, data):
        encrypted = self.fernet.encrypt(data.strip().encode())
        with open(self.path, "ab") as f:
            f.write(encrypted + b"\n")

    def flush(self):
        pass  # Required for stream interface

    def get_handler(self):
        return self.handler

    @staticmethod
    def generate_key():
        return Fernet.generate_key().decode()

    @staticmethod
    def decrypt_file(path, key):
        fernet = Fernet(key.encode())
        with open(path, "rb") as f:
            lines = f.readlines()
        return [fernet.decrypt(line).decode() for line in lines]
