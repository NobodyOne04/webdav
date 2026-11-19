# webdav (filemanager)

JSON file-manager API over one folder: hexagonal core, local-disk and Django 5 adapters (ADR 0003).

## Commands
```sh
make install    # uv sync
make run        # dev server, 127.0.0.1:8000, root data/ (FILEMANAGER_ROOT to change)
make check      # ruff check + ruff format --check + pytest (run before every PR)
make fmt        # ruff format + fixes
```

## Layout
- `src/filemanager/core/`: `domain/` (`RelPath`, `Entry`, errors), `ports/` (`FileStore`),
  `application/` (`FileManager`). No Django, no filesystem calls.
- `src/filemanager/adapters/outbound/local.py`: `LocalFileStore`.
- `src/filemanager/adapters/inbound/web/`: views, urls (specific routes before `<path:path>`).
- `src/filemanager/composition.py`: `file_manager()`; tests clear its cache to swap the root.
- `project/`: Django settings/urls/wsgi; `data/`: the default managed folder.
- `tests/`: `test_core.py`, `test_local_store.py`, `test_web.py`.
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- Every path from a request goes through `RelPath.parse`; `LocalFileStore` checks the real path
  again. Never join request paths onto the root yourself.
- New rules go in `FileManager` with a core test on the in-memory store.
- A new domain error needs an HTTP status in `views.STATUS`.
- No auth: localhost only.
