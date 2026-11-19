from django.urls import path

from filemanager.adapters.inbound.web import views

urlpatterns = [
    path("", views.listing, name="root"),
    path("create/<path:path>", views.create, name="create"),
    path("delete/<path:path>", views.delete, name="delete"),
    path("download/<path:path>", views.download, name="download"),
    path("<path:path>", views.listing, name="listing"),
]
