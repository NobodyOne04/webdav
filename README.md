# webdav

A small Django REST app that manages folders and files under one directory through URLs
(university lab 1, 2019). Despite the name it isn't a WebDAV server: plain HTTP routes.

## Run

```sh
python3 -m venv env && . env/bin/activate
pip install -r requiraments.txt          # Django 2.2, DRF 3.10
python3 manage.py runserver
```

## API

All paths are relative to `fileManager/StaticFolder/`.

| Method | URL | Does |
|---|---|---|
| GET | `/` | list the root folder |
| GET | `/<path>` | list a folder |
| GET | `/create/<path>` | create a folder |
| DELETE | `/delete/<path>` | delete an **empty** folder (files are refused) |
| GET | `/download/<name>` | download a file (the extension may be omitted) |

Responses are JSON (`{"response": "…"}` for messages), downloads are attachments.

**Lab code, not safe to expose**: paths aren't sanitised (`..` leaves the folder), folders are
created with GET, and settings are development-only (`DEBUG = True`, committed `SECRET_KEY`).

Decisions: [docs/adr](docs/adr/README.md).
