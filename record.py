import pyaudio
import wave
import subprocess
import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# === Configuration ====
filename_wav = "lecture.wav"
filename_mp3 = "lecture.mp3"

#---------------ASK USER FOR DURATION-------------------#
duration = 60 * 5  # 5 minutes; change as needed, ASK USER
#-------------------------------------------------------#


chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100

# === Step 1: Record Audio to WAV ===
audio = pyaudio.PyAudio()

stream = audio.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

print("🎙️ Recording... Press Ctrl+C to stop early.")
frames = []

try:
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
except KeyboardInterrupt:
    print("🛑 Stopped manually.")

stream.stop_stream()
stream.close()
audio.terminate()

# Save WAV file
with wave.open(filename_wav, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))

print(f"✅ WAV file saved as {filename_wav}")


# === Step 2: Convert WAV to MP3 with ffmpeg ===
print("🔄 Converting to MP3 using ffmpeg...")


ffmpeg_path = os.getenv("FFMPEG_PATH")  #fallback to system ffmpeg

if not ffmpeg_path:
    raise ValueError("FFMPEG_PATH is not set in the environment variables.")

subprocess.run([
    
    ffmpeg_path, "-y",
    "-i", filename_wav,
    "-vn",
    "-ar", "44100",
    "-ac", "2",
    "-b:a", "192k",
    filename_mp3
], check=True)


print(f"✅ MP3 saved as {filename_mp3}")