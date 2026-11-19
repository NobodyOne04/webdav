"""Composition root: the only place that picks adapters."""

import os
from functools import cache
from pathlib import Path

from filemanager.adapters.outbound.local import LocalFileStore
from filemanager.core.application import FileManager

DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "data"


@cache
def file_manager() -> FileManager:
    """The app's one FileManager over $FILEMANAGER_ROOT (default: the repo's data/ folder)."""
    return FileManager(LocalFileStore(Path(os.environ.get("FILEMANAGER_ROOT", DEFAULT_ROOT))))
