from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

STATIC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), 'StaticFolder'))


def resolve(id):
    """The absolute path for id, or None if it would leave STATIC_PATH (e.g. via '..' or a symlink)."""
    path = os.path.realpath(os.path.join(STATIC_PATH, str(id)))
    return path if os.path.commonpath([path, STATIC_PATH]) == STATIC_PATH else None


def outside(id):
    return Response({'response': 'path ' + str(id) + ' is outside the managed folder'}, status=400)


@api_view(['GET'])
def index(request):
    return Response(os.listdir(STATIC_PATH))

@api_view(['GET'])
def view(request, id):
    path = resolve(id)
    if path is None:
        return outside(id)
    if os.path.isdir(path):
        return Response(os.listdir(path))
    else:
        return Response({'response':'path '+ str(id) + ' is not exist'})

@api_view(['GET'])
def create(request, id):
    dirName = resolve(id)
    if dirName is None:
        return outside(id)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        response = "Directory " + str(id) +  " Created "
    else:
        response = "Directory " + str(id) + " already exists"
    return Response({"response":response})

@api_view(['DELETE'])
def delete(request, id):
    pathToFile = resolve(id)
    if pathToFile is None or pathToFile == STATIC_PATH:
        return outside(id)
    if os.path.exists(pathToFile):
        if os.path.isfile(pathToFile): response = "You try to delete file"
        elif os.listdir(pathToFile) == []:
            os.rmdir(pathToFile)
            response = "Directory " + str(id) +  " Deleted "
        else:
            response = "Directory is not empty"
    else:
        response = "Directory not exists " + str(id)
    return Response({"response":response})

@api_view(['GET'])
def download(request, id):
    for file in os.listdir(STATIC_PATH):
        if id == file.split('.')[0]: id = file
    path_to_file = resolve(id)
    if path_to_file is None:
        return outside(id)
    if os.path.isfile(path_to_file):
        return FileResponse(open(path_to_file, 'rb'), as_attachment=True, filename=os.path.basename(path_to_file))
    else:
        return Response({'response':'path '+str(id)+' is not exist'})
