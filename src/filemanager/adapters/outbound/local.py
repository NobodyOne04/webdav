from pathlib import Path
from typing import BinaryIO

from filemanager.core.domain import Entry, OutsideRoot, RelPath
from filemanager.core.ports import Kind


class LocalFileStore:
    """FileStore on a local folder. Resolves symlinks and refuses anything that lands outside it."""

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def _real(self, path: RelPath) -> Path:
        real = self._root.joinpath(*path.parts).resolve()
        if real != self._root and self._root not in real.parents:
            raise OutsideRoot(str(path))
        return real

    def kind(self, path: RelPath) -> Kind | None:
        real = self._real(path)
        if real.is_dir():
            return "dir"
        if real.is_file():
            return "file"
        return None

    def list(self, path: RelPath) -> list[Entry]:
        return [Entry(p.name, p.is_dir()) for p in self._real(path).iterdir()]

    def make_dir(self, path: RelPath) -> None:
        self._real(path).mkdir()

    def remove_dir(self, path: RelPath) -> None:
        self._real(path).rmdir()

    def open(self, path: RelPath) -> BinaryIO:
        return self._real(path).open("rb")
