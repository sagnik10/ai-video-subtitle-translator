import os

# Inject ffmpeg into PATH for whisper subprocess calls
FFMPEG_DIR = r'C:\Users\nwp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin'
os.environ["PATH"] += os.pathsep + FFMPEG_DIR

import whisper
from transformers import MarianMTModel, MarianTokenizer

whisper_model = whisper.load_model('base')

model_name = 'Helsinki-NLP/opus-mt-en-he'
tokenizer = MarianTokenizer.from_pretrained(model_name)
translator = MarianMTModel.from_pretrained(model_name)

def transcribe_and_translate(audio_path, lang='he'):
    result = whisper_model.transcribe(audio_path, fp16=False)

    segments = []
    for seg in result["segments"]:
        text = seg["text"]

        inputs = tokenizer(text, return_tensors="pt", padding=True)
        output = translator.generate(**inputs)
        hebrew = tokenizer.decode(output[0], skip_special_tokens=True)

        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": hebrew
        })

    return segments
