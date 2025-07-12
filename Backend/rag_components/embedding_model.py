from sentence_transformers import SentenceTransformer

# This module initializes the embedding model, ensuring it's loaded once.
# 'all-MiniLM-L6-v2' is a high-quality, fast, and completely free model
# that runs locally without needing an API key.

print("--- [Embeddings] Loading Sentence Transformer model... (This may take a moment on first run) ---")
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("--- [Embeddings] Model loaded successfully. ---")
except Exception as e:
    print(f"--- [Embeddings] CRITICAL ERROR: Could not load sentence-transformer model. Error: {e}")
    print("--- [Embeddings] Please ensure you have an internet connection for the first download.")
    embedding_model = None