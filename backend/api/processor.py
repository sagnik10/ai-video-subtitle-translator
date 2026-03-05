import threading
from .job_store import jobs
from .translator_engine import translate
from .whisper_engine import transcribe_audio


def process_video(job_id, audio_path, lang):

    jobs[job_id]["stage"] = "transcribing"

    segments = transcribe_audio(audio_path)

    translated_segments = []

    total = len(segments)

    for i, seg in enumerate(segments):

        text = seg["text"]

        translated = translate(text, lang)

        translated_segments.append(translated)

        jobs[job_id]["progress"] = int((i / total) * 100)

        jobs[job_id]["transcription"] = translated

    jobs[job_id]["status"] = "completed"
    jobs[job_id]["stage"] = "finished"


def start_processing(job_id, audio_path, lang):

    thread = threading.Thread(target=process_video, args=(job_id, audio_path, lang))

    thread.start()