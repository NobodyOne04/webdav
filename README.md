# webdav (filemanager)

A small JSON API that manages folders and files under one directory (university lab 1, 2019;
redesigned 2026). Despite the name it isn't a WebDAV server: plain HTTP routes.

## Run

```sh
make install                               # uv sync: Python 3.12+, Django 5.2
make run                                   # http://127.0.0.1:8000, serving data/
FILEMANAGER_ROOT=~/somewhere make run      # serve another folder
make check                                 # ruff lint + format check, pytest
```

## API

Paths are relative to the managed folder (`$FILEMANAGER_ROOT`, default `data/`).

| Method | URL | Does | Success |
|---|---|---|---|
| GET | `/`, `/<path>` | list a folder: `[{"name", "is_dir"}]`, folders first | 200 |
| POST | `/create/<path>` | create a folder | 201 |
| DELETE | `/delete/<path>` | delete an **empty** folder | 200 |
| GET | `/download/<name>` | download a file as an attachment; the extension may be omitted | 200 |

Errors are `{"error": "..."}`: 404 not found, 400 outside the folder or not a folder, 409
already exists / not empty / is a file, 405 wrong method.

## Design

Hexagonal, like [personal-ai](https://github.com/NobodyOne04/personal-ai):

```
src/filemanager/
  core/
    domain/          RelPath (refuses .. and absolute paths), Entry, errors
    ports/           FileStore (kind, list, make_dir, remove_dir, open)
    application/     FileManager: list, create, delete, download and their rules
  adapters/
    outbound/        LocalFileStore: a folder on disk, also refuses symlinks out of it
    inbound/web/     Django views: JSON, errors mapped to HTTP codes
  composition.py     file_manager() over $FILEMANAGER_ROOT
project/             Django settings, urls, wsgi
tests/               core (in-memory store), local store (temp folder), web (test client)
```

Settings come from the environment: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=1`,
`DJANGO_ALLOWED_HOSTS`. No authentication: keep it on localhost.

Decisions: [docs/adr](docs/adr/README.md).
