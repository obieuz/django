from .views import *
from django.urls import path

urlpatterns = [
    path("",get_movies),
    path("meta/",get_meta),
]
