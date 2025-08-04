import os
from faster_whisper import WhisperModel
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

class Transcriber:
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def transcribe_audio(self):
        model = WhisperModel("Systran/faster-whisper-tiny", device="cpu")

        if not os.path.exists(self.audio_path):
            print("❌ File not found:", self.audio_path)
            return None

        segments, info = model.transcribe(self.audio_path)
        full_text = " ".join([segment.text.strip() for segment in segments])

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        docs = text_splitter.create_documents([full_text])
        return docs

    def store_in_mongodb(self, docs):
        if docs is None:
            print("⚠ No documents to store.")
            return

        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not set in .env")

        client = MongoClient(mongo_uri)
        db = client["EZnotes"]
        collection = db["test3"]

        for i, chunk in enumerate(docs):
            collection.insert_one({
                "file_name": os.path.basename(self.audio_path),
                "chunk_index": i,
                "text": chunk.page_content.strip(),
            })

        print(f"✅ Stored {len(docs)} chunks in MongoDB.")
