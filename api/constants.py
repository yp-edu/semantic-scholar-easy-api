"""
Constants for the whole API.
"""

import os

import toml

# Global
try:
    toml_dict = toml.load("/code/pyproject.toml")
    VERSION = toml_dict["project"]["version"]
except FileNotFoundError:
    VERSION = "0.0.0"
X_API_KEY = os.environ.get("X_API_KEY", "")
TMP_FOLDER = "tmp"
