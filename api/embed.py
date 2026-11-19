import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Load tokenizer and model once at startup (cached across invocations)
from tokenizers import Tokenizer
from sentence_transformers import SentenceTransformer

# Initialize FastAPI app
app = FastAPI()

# Load a BERT tokenizer (uses the huggingface tokenizer files)
TOKENIZER = Tokenizer.from_pretrained("bert-base-uncased")

# Load a lightweight MiniLM model for embeddings
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class TextRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    tokens: List[int]
    embedding: List[float]

@app.post("/api/embed", response_model=EmbedResponse)
async def embed(request: TextRequest):
    # Tokenisation (return token ids)
    encoding = TOKENIZER.encode(request.text)
    tokens = encoding.ids

    # Embedding generation (returns numpy array)
    embedding_vec = MODEL.encode(request.text, convert_to_numpy=True)
    # Convert to plain list of floats (rounded for readability)
    embedding = [float(round(v, 6)) for v in embedding_vec.tolist()]

    return EmbedResponse(tokens=tokens, embedding=embedding)
