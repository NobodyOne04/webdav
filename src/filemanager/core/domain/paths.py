from dataclasses import dataclass
from pathlib import PurePosixPath

from filemanager.core.domain.errors import OutsideRoot


@dataclass(frozen=True)
class RelPath:
    """A normalised path inside the managed folder; the root is RelPath(())."""

    parts: tuple[str, ...] = ()

    @classmethod
    def parse(cls, raw: str) -> "RelPath":
        path = PurePosixPath(raw.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            raise OutsideRoot(raw)
        return cls(tuple(p for p in path.parts if p not in ("", ".")))

    @property
    def is_root(self) -> bool:
        return not self.parts

    @property
    def name(self) -> str:
        return self.parts[-1] if self.parts else ""

    def child(self, name: str) -> "RelPath":
        return RelPath((*self.parts, name))

    def __str__(self) -> str:
        return "/".join(self.parts) or "."


@dataclass(frozen=True)
class Entry:
    name: str
    is_dir: bool
