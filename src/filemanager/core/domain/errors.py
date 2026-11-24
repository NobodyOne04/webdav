class FileManagerError(Exception):
    """Base for every rule the file manager enforces."""


class OutsideRoot(FileManagerError):
    """The path would leave the managed folder."""


class NotFound(FileManagerError):
    """Nothing exists at the path."""


class AlreadyExists(FileManagerError):
    """Something already exists at the path."""


class NotEmpty(FileManagerError):
    """Only empty folders can be deleted."""


class NotADirectory(FileManagerError):
    """The path names a file where a folder is needed."""


class IsAFile(FileManagerError):
    """The path names a file where only folders are allowed."""
