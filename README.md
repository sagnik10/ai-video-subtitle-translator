# AI Video Subtitle Translator

An end-to-end **AI powered video subtitle translation system** that automatically:

1. Extracts audio from uploaded videos
2. Transcribes speech using **OpenAI Whisper**
3. Translates subtitles using **MarianMT neural translation models**
4. Generates **SRT subtitles**
5. Burns translated subtitles directly into the video using **FFmpeg**

The system provides a **web interface and REST API built with Django** and tracks job progress in real time.

---

## Overview

This project implements a complete video translation pipeline:

```
Video Upload
      │
      ▼
Audio Extraction (FFmpeg)
      │
      ▼
Speech Recognition (Whisper)
      │
      ▼
Neural Translation (MarianMT)
      │
      ▼
Subtitle Generation (SRT)
      │
      ▼
Video Rendering (FFmpeg)
      │
      ▼
Translated Subtitled Video
```

Users upload a video and receive a **translated version with subtitles embedded into the video**.

---

## Features

* Automatic **speech transcription**
* **Neural machine translation**
* **Subtitle generation**
* **Subtitle rendering into video**
* **Real-time progress tracking**
* **Django admin monitoring**
* **REST API for job tracking**
* Background processing using threads
* Supports multiple target languages

---

## Technology Stack

Backend Framework

* Django
* Django REST Framework

AI Models

* Whisper (Speech Recognition)
* MarianMT (Neural Machine Translation)

Video Processing

* FFmpeg

Frontend

* HTML
* TailwindCSS
* JavaScript

Other Tools

* Python
* Transformers (HuggingFace)

---

## Supported Translation Languages

Currently supported:

* Hebrew
* French
* Spanish

Additional MarianMT models can easily be added.

---

## Project Structure

```
video-translator/
│
├── api/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── whisper_engine.py
│   ├── translator_engine.py
│   ├── srt_generator.py
│   ├── admin.py
│
├── templates/
│   └── index.html
│
├── media/
│   ├── uploads/
│   └── outputs/
│
├── manage.py
└── requirements.txt
```

---

## Installation

### 1. Clone Repository

```
git clone https://github.com/sagnik10/ai-video-subtitle-translator.git
cd ai-video-subtitle-translator
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Linux / macOS

```
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

Required major packages:

* django
* djangorestframework
* torch
* transformers
* openai-whisper

---

### 4. Install FFmpeg

Download from:

```
https://ffmpeg.org/download.html
```

Ensure FFmpeg is available in your system path.

---

### 5. Run Database Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Admin User

```
python manage.py createsuperuser
```

---

### 7. Run Server

```
python manage.py runserver
```

Or specify port:

```
python manage.py runserver 8001
```

Open:

```
http://127.0.0.1:8001
```

---

## API Endpoints

### Upload Video

```
POST /api/upload/
```

Form Data

```
file : video file
language : target language
```

Response

```
{
  "job_id": "uuid"
}
```

---

### Job Status

```
GET /api/status/<job_id>/
```

Example Response

```
{
  "status": "processing",
  "stage": "transcribing",
  "progress": 40,
  "transcription": "...",
  "video_url": ""
}
```

---

## Admin Panel

Django admin provides monitoring of all jobs.

Open:

```
http://127.0.0.1:8001/admin
```

The admin panel shows:

* Uploaded video
* Generated video
* Job progress
* Processing stage
* Transcription
* Creation time

---

## Media Storage

Videos and intermediate files are stored inside:

```
media/
```

Structure:

```
media/
   uploads/
      input_video.mp4

   outputs/
      subtitled_video.mp4

   input_video.mp4.wav
   input_video.mp4.srt
```

Database stores **file paths**, not the video itself.

---

## Processing Stages

Jobs progress through the following stages:

```
uploading
extracting_audio
transcribing
rendering_video
completed
```

Each stage updates job progress.

---

## Future Improvements

Potential enhancements include:

* GPU accelerated Whisper inference
* Celery background workers
* Redis job queues
* S3 video storage
* WebSocket live progress updates
* Multi-language subtitle tracks
* Subtitle styling customization

---

## License

Apache License 2.0

```
Copyright 2026 Sagnik

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this project except in compliance with the License.

You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an **"AS IS" BASIS**, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.

---

## Author

Sagnik

GitHub

https://github.com/sagnik10

---

## Acknowledgements

* OpenAI Whisper
* HuggingFace Transformers
* MarianMT translation models
* FFmpeg multimedia framework
* Django web framework

---
