from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import BinaryIO

from filemanager.core.domain import (
    AlreadyExists,
    Entry,
    IsAFile,
    NotADirectory,
    NotEmpty,
    NotFound,
    RelPath,
)
from filemanager.core.ports import FileStore


@dataclass
class Download:
    name: str
    content: BinaryIO


class FileManager:
    """The operations and their rules; all storage goes through the FileStore port."""

    def __init__(self, store: FileStore) -> None:
        self._store = store

    def list(self, raw: str = "") -> list[Entry]:
        path = RelPath.parse(raw)
        kind = self._store.kind(path)
        if kind is None:
            raise NotFound(str(path))
        if kind == "file":
            raise NotADirectory(str(path))
        return sorted(self._store.list(path), key=lambda e: (not e.is_dir, e.name))

    def create(self, raw: str) -> RelPath:
        path = RelPath.parse(raw)
        if path.is_root or self._store.kind(path) is not None:
            raise AlreadyExists(str(path))
        parent = RelPath(path.parts[:-1])
        if self._store.kind(parent) != "dir":
            raise NotFound(str(parent))
        self._store.make_dir(path)
        return path

    def delete(self, raw: str) -> RelPath:
        path = RelPath.parse(raw)
        kind = self._store.kind(path)
        if path.is_root or kind is None:
            raise NotFound(str(path))
        if kind == "file":
            raise IsAFile(str(path))
        if self._store.list(path):
            raise NotEmpty(str(path))
        self._store.remove_dir(path)
        return path

    def download(self, raw: str) -> Download:
        """A file by path; a bare name without extension matches a root file with that stem."""
        path = RelPath.parse(raw)
        if self._store.kind(path) != "file" and len(path.parts) == 1:
            path = self._by_stem(path.name) or path
        if self._store.kind(path) != "file":
            raise NotFound(str(path))
        return Download(path.name, self._store.open(path))

    def _by_stem(self, stem: str) -> RelPath | None:
        for entry in self.list():
            if not entry.is_dir and PurePosixPath(entry.name).stem == stem:
                return RelPath((entry.name,))
        return None
