from functools import wraps

from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from filemanager.composition import file_manager
from filemanager.core.domain import (
    AlreadyExists,
    FileManagerError,
    IsAFile,
    NotADirectory,
    NotEmpty,
    NotFound,
    OutsideRoot,
)

STATUS = {
    NotFound: 404,
    OutsideRoot: 400,
    NotADirectory: 400,
    AlreadyExists: 409,
    NotEmpty: 409,
    IsAFile: 409,
}


def json_api(*methods):
    """Allowed methods, no CSRF (JSON API, no cookies), domain errors as JSON with a status."""

    def decorate(view):
        @csrf_exempt
        @require_http_methods(list(methods))
        @wraps(view)
        def wrapper(request, path=""):
            try:
                return view(request, path)
            except FileManagerError as error:
                message = f"{type(error).__name__}: {error}"
                return JsonResponse({"error": message}, status=STATUS[type(error)])

        return wrapper

    return decorate


@json_api("GET")
def listing(request, path):
    entries = file_manager().list(path)
    return JsonResponse([{"name": e.name, "is_dir": e.is_dir} for e in entries], safe=False)


@json_api("POST")
def create(request, path):
    return JsonResponse({"created": str(file_manager().create(path))}, status=201)


@json_api("DELETE")
def delete(request, path):
    return JsonResponse({"deleted": str(file_manager().delete(path))})


@json_api("GET")
def download(request, path):
    found = file_manager().download(path)
    return FileResponse(found.content, as_attachment=True, filename=found.name)
