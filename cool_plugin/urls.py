from django.contrib import admin
from django.urls import path, re_path
from .views import UserManager

urlpatterns = [
    re_path(r'^user', UserManager.as_view(), name='user'),
]
