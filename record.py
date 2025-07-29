import pyaudio
import wave
import subprocess

# === Configuration ===
filename_wav = "lecture.wav"
filename_mp3 = "lecture.mp3"
duration = 60 * 5  # 5 minutes; change as needed
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

subprocess.run([
    "C:\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe", "-y",  # Overwrite if exists
    "-i", filename_wav,
    "-vn",  # No video
    "-ar", "44100",  # Sample rate
    "-ac", "2",      # Stereo
    "-b:a", "192k",  # Bitrate
    filename_mp3
], check=True)

print(f"✅ MP3 saved as {filename_mp3}")