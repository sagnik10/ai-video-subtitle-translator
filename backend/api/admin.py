from django.contrib import admin
from .models import VideoJob


@admin.register(VideoJob)
class VideoJobAdmin(admin.ModelAdmin):

    list_display = (
        "job_id",
        "status",
        "stage",
        "progress",
        "input_video",
        "output_video",
        "created_at"
    )

    search_fields = ("job_id",)

    list_filter = (
        "status",
        "stage"
    )

    ordering = ("-created_at",)