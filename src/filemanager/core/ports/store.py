from typing import BinaryIO, Literal, Protocol

from filemanager.core.domain import Entry, RelPath

Kind = Literal["dir", "file"]


class FileStore(Protocol):
    """Storage for the managed folder. Implementations must never touch anything outside it."""

    def kind(self, path: RelPath) -> Kind | None: ...

    def list(self, path: RelPath) -> list[Entry]: ...

    def make_dir(self, path: RelPath) -> None: ...

    def remove_dir(self, path: RelPath) -> None: ...

    def open(self, path: RelPath) -> BinaryIO: ...
