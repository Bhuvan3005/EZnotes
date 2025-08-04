from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from record import AudioRecorder
from models.transcirbe import Transcriber
from models.summarize import Summarizer  

app = FastAPI()
recorder = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecordParams(BaseModel):
    duration: int
    filename: str


@app.post("/start-recording")
def start_recording(params: RecordParams):
    global recorder
    try:
        recorder = AudioRecorder(
            wav_filename=f"{params.filename}.wav",
            mp3_filename=f"{params.filename}.mp3",
            duration=params.duration
        )
        recorder.start()
        
        return {"message": f"Recording started for {params.duration} seconds"}
    except Exception as e:
        print(" Error in /start-recording:", e)
        return {"error": str(e)}


@app.post("/stop-recording")
def stop_recording():
    global recorder
    if recorder:
        recorder.stop()
        recorder._save_wav()
        recorder._convert_to_mp3()
        return {"message": "Recording stopped and saved"}
    return {"message": "No recording in progress"}

@app.post("/transcribe")
def transcribe_audio(params: RecordParams):
    global transcriber
    try:    
        
        transcriber= Transcriber(audio_path=params.filename + ".mp3")
        docs = transcriber.transcribe_audio()
        transcriber.store_in_mongodb(docs)
        return {"message": "Transcription completed and stored in MongoDB"}
    except Exception as e:
        print(" Error in /transcribe:", e)
        return {"error": str(e)}
          
    
@app.post("/summarize")
def summarize_audio(params: RecordParams):
    try:
        summarizer = Summarizer(audio_path=params.filename + ".mp3")
        summary = summarizer.summarize_audio()
        if summary:
            print("🔍 Finalll Summary:\n", summary)
            return {"summary": summary}
            
        else:
            return {"message": "No summary generated"}
    except Exception as e:
        print(" Error in /summarize:", e)
        return {"error": str(e)}
