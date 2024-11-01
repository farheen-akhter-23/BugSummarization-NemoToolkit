from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from services.summarize import generate_summary
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility
)
from sentence_transformers import SentenceTransformer
import uuid

app = FastAPI()

# Define the Milvus connection and collection setup
os.makedirs("milvus_lite", exist_ok=True)
MILVUS_URI = "./milvus_lite/milvus_vector.db"
connections.connect("default", uri=MILVUS_URI)
print(f"Connected to Milvus at {MILVUS_URI}")
collection_name = "bug_reports"

# Initialize the model for generating embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define schema for Milvus
if not utility.has_collection(collection_name):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="summary", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384)  # Add vector field
    ]
    schema = CollectionSchema(fields, description="Bug Report Summaries")
    collection = Collection(name=collection_name, schema=schema, consistency_level="Strong")
    print(f"Created collection '{collection_name}'.")

class BugReportRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize_text(request: BugReportRequest):
    text = request.text
    summary = generate_summary(text)
    
    # Generate vector embedding
    vector = embedding_model.encode(text).tolist()
    
    # Save to Milvus
    doc_id = int(uuid.uuid4().int & (1<<64)-1)
    collection.insert([{"id": doc_id, "text": text, "summary": summary, "vector": vector}])

    return {"summary": summary}

@app.get("/history")
async def get_history():
    # Fetch summaries from Milvus
    collection.load()
    history = [{"text": doc["text"], "summary": doc["summary"]} for doc in collection.query(expr=None, limit=10)]
    return history
