from django.urls import include, path

urlpatterns = [path("", include("filemanager.adapters.inbound.web.urls"))]
