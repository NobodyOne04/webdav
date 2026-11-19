# Changelog

## Unreleased

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
