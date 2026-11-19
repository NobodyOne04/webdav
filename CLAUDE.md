# webdav

A 2019 university lab: Django + DRF routes to list, create, delete and download files in one folder.

## Commands
```sh
pip install -r requiraments.txt        # note the spelling
python3 manage.py runserver
```
`fileManager/tests.py` is the empty Django stub.

## Layout
- `Lab/`: Django project (settings, root urls, wsgi).
- `fileManager/views.py`: the five DRF function views; `fileManager/urls.py`: routes.
- `fileManager/StaticFolder/`: the managed folder (`test.txt` sample).
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- Not safe to expose (path traversal, GET creates, dev settings): keep it local.
- Archived lab: docs or small fixes only unless asked.
