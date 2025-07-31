from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["EZnotes"]
collection = db["test3"]


groq_api_key = os.getenv("GROQ_API_KEY") 


# STEP 2: Retrieve stored chunks
chunk_texts = [doc["text"] for doc in collection.find({"file_name":"lecture.mp3"}, {"_id": 0, "text": 1})]

if not chunk_texts:
    raise ValueError("No chunks found for 'audio.mp3' in the database.")

# STEP 3: Wrap each chunk in a LangChain Document

docs = [Document(page_content=chunk_texts[i], metadata={"chunk_index": i}) for i in range(len(chunk_texts))]
##docs = [Document(page_content=full_text)]

# STEP 4: Initialize ChatGroq with Gemma
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="gemma2-9b-it"
)

# STEP 5: Load refine summarization chain
chain = load_summarize_chain(llm, chain_type="refine")

# STEP 6: Run summarization
summary = chain.run(docs)

# STEP 7: Print or return the summary
print("\n🔍 Final Summary:\n")
print(summary)
