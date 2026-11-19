"""Django settings for the web adapter; deployment specifics come from the environment."""

import os

from django.core.management.utils import get_random_secret_key

# without DJANGO_SECRET_KEY each start gets a random key
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()
DEBUG = os.environ.get("DJANGO_DEBUG", "") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = ["filemanager.adapters.inbound.web"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]
ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"
DATABASES: dict = {}  # nothing is stored besides the files themselves
USE_TZ = True
