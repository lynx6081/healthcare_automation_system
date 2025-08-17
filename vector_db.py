import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_DIR = "./vectordb/faiss_vectors"
META_FILE = "./vectordb/faiss_metadata.pkl"
os.makedirs(VECTOR_DIR, exist_ok=True)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
EMBED_DIM = embed_model.get_sentence_embedding_dimension()

index_file = os.path.join(VECTOR_DIR, "index.faiss")
if os.path.exists(index_file):
    index = faiss.read_index(index_file)
else:
    index = faiss.IndexFlatL2(EMBED_DIM)

if os.path.exists(META_FILE):
    with open(META_FILE, "rb") as f:
        metadata = pickle.load(f)
else:
    metadata = {}

next_id = len(metadata)

def save_index():
    faiss.write_index(index, index_file)
    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)

def add_or_update_profile(user_id, profile_data):
    global next_id
    content = str(profile_data)
    embedding = embed_model.encode(content).astype("float32")
    index.add(np.array([embedding]))
    metadata[user_id] = next_id
    next_id += 1
    save_index()

def retrieve_profile(user_id):
    if user_id not in metadata:
        return {}
    return {"user_id": user_id, "info": "Profile stored"}  # store real profile if needed
