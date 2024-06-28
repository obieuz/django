from .views import *
from django.urls import path

urlpatterns = [
    path("get/",getMovies, name="get"),
    path("meta/",getMeta, name="getMeta"),
]
