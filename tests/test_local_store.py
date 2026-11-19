"""LocalFileStore on a real temporary folder."""

import pytest

from filemanager.adapters.outbound.local import LocalFileStore
from filemanager.core.application import FileManager
from filemanager.core.domain import Entry, OutsideRoot, RelPath


@pytest.fixture
def root(tmp_path):
    (tmp_path / "root").mkdir()
    (tmp_path / "root" / "f.bin").write_bytes(b"\x00\xff")
    (tmp_path / "secret.txt").write_text("outside")
    return tmp_path / "root"


def test_round_trip(root):
    fm = FileManager(LocalFileStore(root))
    fm.create("d")
    assert fm.list() == [Entry("d", True), Entry("f.bin", False)]
    assert fm.download("f").content.read() == b"\x00\xff"
    fm.delete("d")
    assert not (root / "d").exists()


def test_a_symlink_out_of_the_root_is_refused(root):
    (root / "escape").symlink_to(root.parent / "secret.txt")
    store = LocalFileStore(root)
    with pytest.raises(OutsideRoot):
        store.open(RelPath(("escape",)))
