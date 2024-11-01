from pymilvus import Collection, connections
import os


os.makedirs("milvus_lite", exist_ok=True)
MILVUS_URI = "./milvus_lite/milvus_vector.db"
connections.connect("default", uri=MILVUS_URI)
print(f"Connected to Milvus at {MILVUS_URI}")

def get_milvus_collection(collection_name="bug_reports"):
    # Initialize or retrieve the Milvus collection for bug reports
    collection = Collection(name=collection_name)
    return collection