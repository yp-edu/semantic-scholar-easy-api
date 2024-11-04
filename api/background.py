"""
Background tasks for the app.
"""

import logging
import subprocess

from api.constants import TMP_FOLDER


def clean_folder(folder_id: str):
    """
    Clean the folder with the given id.
    """
    logger = logging.getLogger("uvicorn")
    logger.info(f"Cleaning folder {folder_id}...")
    rm_cmd = ["rm", "-r", f"{TMP_FOLDER}/{folder_id}"]
    result = subprocess.run(rm_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(result.stderr.decode("utf8"))
