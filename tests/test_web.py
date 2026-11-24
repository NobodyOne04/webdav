"""The Django adapter through the test client, on a temporary root."""

import pytest
from django.test import Client

from filemanager import composition


@pytest.fixture
def client(tmp_path, monkeypatch):
    (tmp_path / "test.txt").write_text("hello")
    monkeypatch.setenv("FILEMANAGER_ROOT", str(tmp_path))
    composition.file_manager.cache_clear()
    yield Client()
    composition.file_manager.cache_clear()


def test_list(client):
    assert client.get("/").json() == [{"name": "test.txt", "is_dir": False}]


def test_create_list_delete(client):
    assert client.post("/create/d").status_code == 201
    assert client.get("/d").json() == []
    assert client.delete("/delete/d").json() == {"deleted": "d"}


def test_create_needs_post(client):
    assert client.get("/create/d").status_code == 405


def test_download_by_stem(client):
    response = client.get("/download/test")
    assert response.status_code == 200
    assert b"".join(response.streaming_content) == b"hello"
    assert 'filename="test.txt"' in response["Content-Disposition"]


@pytest.mark.parametrize(
    "method, url, status",
    [
        ("get", "/nope", 404),
        ("get", "/..%2F..%2Fetc", 400),
        ("post", "/create/..%2Fx", 400),
        ("delete", "/delete/test.txt", 409),
        ("get", "/download/missing", 404),
    ],
)
def test_errors_are_json_with_status(client, method, url, status):
    response = getattr(client, method)(url)
    assert response.status_code == status
    assert "error" in response.json()
