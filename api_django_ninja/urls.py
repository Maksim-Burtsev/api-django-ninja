from django.contrib import admin
from django.urls import path

from main.api import api as main_api
from eng.api import api as eng_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", main_api.urls),
    path("eng_api/", eng_api.urls)
]
