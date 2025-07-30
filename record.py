# audio_recorder.py
import threading
import wave
import pyaudio
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

class AudioRecorder:
    def __init__(self, wav_filename="lecture.wav", mp3_filename="lecture.mp3", duration=60):
        self.wav_filename = wav_filename
        self.mp3_filename = mp3_filename
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.frames = []
        self.recording = False
        self.thread = None
        self.audio = pyaudio.PyAudio()
        self.duration = duration

    def _record(self):
        print("🎙 Recording started...")
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)

        self.frames = []
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

        self._save_wav()
        self._convert_to_mp3()

        print("✅ Recording stopped and saved.")

    def start(self):
        if self.recording:
            print("⚠ Already recording.")
            return
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop(self):
        if not self.recording:
            print("⚠ Not recording.")
            return
        self.recording = False
        self.thread.join()

    def _save_wav(self):
        with wave.open(self.wav_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        print(f"💾 WAV file saved as {self.wav_filename}")

    def _convert_to_mp3(self):
        ffmpeg_path = os.getenv("FFMPEG_PATH")
        if not ffmpeg_path:
            raise ValueError("FFMPEG_PATH is not set in the environment variables.")

        subprocess.run([
            ffmpeg_path, "-y",
            "-i", self.wav_filename,
            "-vn",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",
            self.mp3_filename
        ], check=True)

        print(f"🎧 MP3 file saved as {self.mp3_filename}")
