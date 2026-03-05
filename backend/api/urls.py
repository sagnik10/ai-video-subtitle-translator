from django.contrib import admin
from django.urls import path
from api.views import UploadVideoView, StatusView, home

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/upload/", UploadVideoView.as_view()),
    path("api/status/<str:job_id>/", StatusView.as_view()),
]