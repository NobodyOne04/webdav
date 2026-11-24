# Changelog

## Unreleased

### Changed
- Redesigned hexagonally (ADR 0003): framework-free core with a `FileStore` port, local-disk and Django 5.2 adapters; Python 3.12+ with uv, ruff and pytest
- `create` is `POST` (was GET); errors are JSON with proper status codes; listings show `name` and `is_dir`, folders first
- The managed folder is `data/` (or `FILEMANAGER_ROOT`), was `fileManager/StaticFolder/`

### Removed
- Django REST framework and the old `Lab` / `fileManager` Django layout

### Added
- README in English, CLAUDE.md, changelog and ADRs

### Fixed
- Paths with `..` or symlinks could reach files outside the managed folder; they are now refused with 400
- Downloads were opened as text with a fixed type and file name; now binary with the real name
- `SECRET_KEY` was committed; it now comes from `DJANGO_SECRET_KEY` (random per start without it)

### Added
- Tests for listing, downloads, create/view/delete and path traversal

### Changed
- Default branch renamed from `master` to `main`
