# test_embedding.py
from rbd.model_loader import get_embedding_model

model = get_embedding_model()
vec = model.create_embedding("Hello, world!")["data"][0]["embedding"]
print(f"Embedding length: {len(vec)}")  # Should be 768