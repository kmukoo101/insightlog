"""
Configuration Loader for InsightLog

Supports:
- JSON / YAML config file loading
- Environment variable overrides
- Default fallback values
"""

import os
import json

try:
    import yaml
except ImportError:
    yaml = None


DEFAULT_CONFIG = {
    "log_level": "INFO",
    "log_format": "json",  # or "plain"
    "redact_patterns": ["AKIA[0-9A-Z]{16}", "password=.*"],
    "entropy_threshold": 4.2,
    "log_file": "insightlog_output.log",
    "enable_encryption": False,
    "encryption_password": None
}


def load_config(path=None):
    """
    Load logging configuration from file or environment variables.

    Args:
        path (str): Path to a YAML or JSON config file.

    Returns:
        dict: Final config dictionary
    """
    config = DEFAULT_CONFIG.copy()

    if path and os.path.exists(path):
        ext = os.path.splitext(path)[-1].lower()
        try:
            with open(path, "r") as f:
                if ext == ".json":
                    file_config = json.load(f)
                elif ext in [".yaml", ".yml"] and yaml:
                    file_config = yaml.safe_load(f)
                else:
                    raise ValueError("Unsupported config format")
                config.update({k: v for k, v in file_config.items() if k in DEFAULT_CONFIG})
        except Exception as e:
            print(f"[InsightLog] Error loading config: {e}")

    # Check for environment variable overrides
    for key in DEFAULT_CONFIG:
        env_var = f"INSIGHTLOG_{key.upper()}"
        if env_var in os.environ:
            val = os.environ[env_var]
            # Try casting to appropriate type
            if isinstance(DEFAULT_CONFIG[key], bool):
                config[key] = val.lower() in ("1", "true", "yes")
            elif isinstance(DEFAULT_CONFIG[key], (int, float)):
                try:
                    config[key] = type(DEFAULT_CONFIG[key])(val)
                except Exception:
                    pass
            else:
                config[key] = val

    return config
