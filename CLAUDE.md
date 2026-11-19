# webdav

A 2019 university lab: Django + DRF routes to list, create, delete and download files in one folder.

## Commands
```sh
pip install -r requiraments.txt        # note the spelling
python3 manage.py runserver
python3 manage.py test fileManager   # list, download, create/view/delete, traversal refused
```

## Layout
- `Lab/`: Django project (settings, root urls, wsgi).
- `fileManager/views.py`: the five DRF function views; `fileManager/urls.py`: routes.
- `fileManager/StaticFolder/`: the managed folder (`test.txt` sample).
- `docs/adr/`: decision records (`.adr`), index in `docs/adr/README.md`.

## Conventions
- Read the ADR before changing a recorded decision; commit subjects carry its number.
- Every path goes through `resolve()` in `views.py`, which refuses anything outside `StaticFolder`.
- Keep it local: GET creates folders and `DEBUG = True`. `SECRET_KEY` comes from `DJANGO_SECRET_KEY`.
- Archived lab: docs or small fixes only unless asked.
