"""The core alone, over an in-memory store."""

import io

import pytest

from filemanager.core.application import FileManager
from filemanager.core.domain import (
    AlreadyExists,
    Entry,
    IsAFile,
    NotADirectory,
    NotEmpty,
    NotFound,
    OutsideRoot,
    RelPath,
)


class MemoryStore:
    def __init__(self, dirs=(), files=None):
        self.dirs = {(), *(tuple(d.split("/")) for d in dirs)}
        self.files = {tuple(k.split("/")): v for k, v in (files or {}).items()}

    def kind(self, path):
        return "dir" if path.parts in self.dirs else "file" if path.parts in self.files else None

    def list(self, path):
        n = len(path.parts)
        kids = {p for p in self.dirs | set(self.files) if len(p) == n + 1 and p[:n] == path.parts}
        return [Entry(p[-1], p in self.dirs) for p in kids]

    def make_dir(self, path):
        self.dirs.add(path.parts)

    def remove_dir(self, path):
        self.dirs.remove(path.parts)

    def open(self, path):
        return io.BytesIO(self.files[path.parts])


@pytest.fixture
def fm():
    return FileManager(
        MemoryStore(dirs=["docs", "empty"], files={"test.txt": b"hi", "docs/a.md": b"#"})
    )


@pytest.mark.parametrize("raw", ["../x", "/etc", "a/../../b", "..\\x"])
def test_paths_outside_the_root_are_refused(raw):
    with pytest.raises(OutsideRoot):
        RelPath.parse(raw)


def test_paths_are_normalised():
    assert RelPath.parse("./docs//a.md").parts == ("docs", "a.md")
    assert RelPath.parse("").is_root


def test_list_puts_folders_first(fm):
    assert fm.list() == [Entry("docs", True), Entry("empty", True), Entry("test.txt", False)]
    assert fm.list("docs") == [Entry("a.md", False)]


def test_list_errors(fm):
    with pytest.raises(NotFound):
        fm.list("nope")
    with pytest.raises(NotADirectory):
        fm.list("test.txt")


def test_create(fm):
    assert str(fm.create("docs/new")) == "docs/new"
    assert Entry("new", True) in fm.list("docs")
    with pytest.raises(AlreadyExists):
        fm.create("docs")
    with pytest.raises(NotFound):
        fm.create("missing/child")


def test_delete_only_empty_folders(fm):
    with pytest.raises(NotEmpty):
        fm.delete("docs")
    with pytest.raises(IsAFile):
        fm.delete("test.txt")
    with pytest.raises(NotFound):
        fm.delete("")
    fm.delete("empty")
    assert Entry("empty", True) not in fm.list()


def test_download_by_path_or_by_stem(fm):
    assert fm.download("test.txt").content.read() == b"hi"
    found = fm.download("test")
    assert found.name == "test.txt" and found.content.read() == b"hi"
    assert fm.download("docs/a.md").name == "a.md"
    with pytest.raises(NotFound):
        fm.download("docs")
