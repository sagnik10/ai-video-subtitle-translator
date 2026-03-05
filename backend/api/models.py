from django.db import models


class VideoJob(models.Model):

    job_id = models.CharField(max_length=100, unique=True)

    status = models.CharField(max_length=20)
    stage = models.CharField(max_length=50)

    progress = models.IntegerField(default=0)

    transcription = models.TextField(blank=True)

    input_video = models.FileField(upload_to="uploads/", null=True, blank=True)

    output_video = models.FileField(upload_to="outputs/", null=True, blank=True)

    video_url = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_id