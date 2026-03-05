import subprocess

FFMPEG_PATH = r'C:\Users\nwp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe'

def extract_audio(video_path, audio_path):
    command = [
        FFMPEG_PATH,
        '-y',
        '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        audio_path
    ]
    subprocess.run(command, check=True)
