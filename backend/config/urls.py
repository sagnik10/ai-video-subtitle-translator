from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.views import UploadVideoView, StatusView, home


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),

    path("api/upload/", UploadVideoView.as_view()),
    path("api/status/<str:job_id>/", StatusView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)