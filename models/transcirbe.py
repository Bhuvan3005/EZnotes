import os
from faster_whisper import WhisperModel
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()


# Load model
model = WhisperModel("Systran/faster-whisper-tiny")

# Audio file
audio_path = "lecture.mp3"

if not os.path.exists(audio_path):
    print("❌ File not found:", audio_path)
    exit()

# Transcribe
segments, info = model.transcribe(audio_path)
full_text = " ".join([segment.text.strip() for segment in segments])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # Adjust chunk size as needed
    chunk_overlap=200,  # Adjust overlap as needed 
)

docs = text_splitter.create_documents([full_text])

mongo_uri = os.getenv("MONGO_URI")
print(mongo_uri)

client = MongoClient(mongo_uri)
db = client["EZnotes"]
collection = db["test3"]

# Save chunks with index
for i, chunk in enumerate(docs):
    collection.insert_one({
        
        "file_name": os.path.basename(audio_path),
        "chunk_index": i,
        "text": chunk.page_content.strip(),
    })

print(f"✅ Stored {len(docs)} chunks in MongoDB.")




