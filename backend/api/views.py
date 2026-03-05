import os
import subprocess
import uuid
import threading
import textwrap

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import VideoJob
from .utils import extract_audio
from .whisper_engine import transcribe_and_translate


FFMPEG_PATH = r'C:\Users\nwp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'


def home(request):
    return render(request, "index.html")


class UploadVideoView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        if "file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        video = request.FILES["file"]
        lang = request.data.get("language", "he")

        job_id = str(uuid.uuid4())

        job = VideoJob.objects.create(
            job_id=job_id,
            status="processing",
            stage="uploading",
            progress=0,
            transcription="",
            input_video=video
        )

        video_path = job.input_video.path
        filename = os.path.basename(video_path)

        thread = threading.Thread(
            target=process_video,
            args=(job_id, video_path, filename, lang)
        )

        thread.start()

        return JsonResponse({"job_id": job_id})


class StatusView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, job_id):

        try:

            job = VideoJob.objects.get(job_id=job_id)

            return JsonResponse({
                "status": job.status,
                "stage": job.stage,
                "progress": job.progress,
                "transcription": job.transcription,
                "video_url": job.output_video.url if job.output_video else ""
            })

        except VideoJob.DoesNotExist:

            return JsonResponse({"error": "Invalid job id"}, status=404)


def process_video(job_id, video_path, filename, lang):

    try:

        job = VideoJob.objects.get(job_id=job_id)

        job.stage = "extracting_audio"
        job.progress = 10
        job.save()

        audio_path = video_path + ".wav"

        extract_audio(video_path, audio_path)

        job.stage = "transcribing"
        job.progress = 25
        job.save()

        segments = transcribe_and_translate(audio_path, lang)

        srt_filename = filename + ".srt"
        srt_path = os.path.join(settings.MEDIA_ROOT, srt_filename)

        with open(srt_path, "w", encoding="utf-8") as srt:

            total = len(segments)

            for i, seg in enumerate(segments, 1):

                progress = 25 + int((i / total) * 50)

                job.progress = progress
                job.transcription = seg["text"]
                job.save(update_fields=["progress", "transcription"])

                srt.write(f"{i}\n")
                srt.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")

                lines = "\n".join(textwrap.wrap(seg["text"], width=45))
                srt.write(f"{lines}\n\n")

        job.stage = "rendering_video"
        job.progress = 80
        job.save()

        output_video = "subtitled_" + filename
        output_path = os.path.join(settings.MEDIA_ROOT, "outputs", output_video)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        subtitle_style = (
            "Alignment=2,"
            "Fontsize=20,"
            "PrimaryColour=&Hffffff&,"
            "OutlineColour=&H000000&,"
            "BorderStyle=3,"
            "Outline=2,"
            "Shadow=1,"
            "MarginV=10"
        )

        subtitle_filter = f"subtitles={srt_filename}:force_style='{subtitle_style}'"

        header_text = "English to Hebrew"

        header_filter = (
            "drawtext="
            f"text='{header_text}':"
            "fontfile='C\\:\\\\Windows\\\\Fonts\\\\arial.ttf':"
            "fontcolor=white:"
            "fontsize=42:"
            "box=1:"
            "boxcolor=black@0.6:"
            "boxborderw=12:"
            "x=(w-text_w)/2:"
            "y=30"
        )

        full_filter = f"{subtitle_filter},{header_filter}"

        command = [
            FFMPEG_PATH,
            "-y",
            "-i",
            filename,
            "-vf",
            full_filter,
            "-c:a",
            "copy",
            output_video
        ]

        subprocess.run(command, check=True, cwd=settings.MEDIA_ROOT)

        job.progress = 100
        job.stage = "completed"
        job.status = "completed"

        job.output_video.name = "outputs/" + output_video
        job.save()

    except Exception as e:

        job = VideoJob.objects.get(job_id=job_id)

        job.status = "error"
        job.stage = "failed"
        job.transcription = str(e)

        job.save()


def format_time(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hrs:02}:{mins:02}:{secs:06.3f}".replace(".", ",")