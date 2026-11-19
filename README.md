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

Responses are JSON (`{"response": "…"}` for messages), downloads are binary attachments
with the real file name. Paths that would leave the folder (`..`, symlinks) get `400`.

Still a lab, keep it local: folders are created with GET and `DEBUG = True`. Set
`DJANGO_SECRET_KEY` if it ever runs anywhere else (otherwise each start uses a random key).

Tests: `python3 manage.py test fileManager`.

Decisions: [docs/adr](docs/adr/README.md).
