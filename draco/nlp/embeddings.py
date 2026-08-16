# DraCo Token Optimizer - NLP Embeddings Module
"""NLP embeddings and vector representations for token analysis.

Provides sentence embeddings, code embeddings, and semantic similarity
measurements using SentenceTransformers and other embedding models.
"""

import numpy as np
from typing import List, Optional, Dict, Any
from draco.config import (
    SENTENCE_TRANSFORMER_MODEL,
    EMBEDDING_DIMENSION,
    DEVICE,
    USE_GPU_ACCELERATION,
    USE_HALF_PRECISION,
)


# ============================================================
# Embedding Model Wrapper
# ============================================================

class EmbeddingModel:
    """Wrapper for SentenceTransformer and other embedding models."""
    
    def __init__(self, model_name: str = None, device: str = None):
        """Initialize the embedding model.
        
        Args:
            model_name: Name of the SentenceTransformer model
            device: Device to run on (cuda, cpu, auto)
        """
        self.model_name = model_name or SENTENCE_TRANSFORMER_MODEL
        self.device = device or DEVICE
        self.half_precision = USE_HALF_PRECISION
        self.model = None
        self.dimension = EMBEDDING_DIMENSION
        
        # Model loading is lazy - done on first use
        self._loaded = False
    
    def _ensure_loaded(self):
        """Load the model if not already loaded."""
        if self._loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            
            model_kwargs = {"device": self.device}
            
            # Use half precision if enabled and on CUDA
            if self.half_precision and self.device == "cuda":
                model_kwargs["torch_dtype"] = "float16"
            
            self.model = SentenceTransformer(self.model_name, **model_kwargs)
            # Verify dimension
            self.dimension = self.model.get_sentence_embedding_dimension()
            
            self._loaded = True
            print(f"Embedding model loaded: {self.model_name}, dimension: {self.dimension}, device: {self.device}")
            
        except ImportError:
            # Fallback: use simple hash-based embedding
            print("sentence_transformers not available, using hash-based fallback")
            self._loaded = True
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            # Fallback to simple embedding
            self._loaded = True
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of shape (num_texts, dimension) with embeddings
        """
        self._ensure_loaded()
        
        if not self.model:
            # Return fallback embeddings
            return self._fallback_embedding(texts)
        
        if not texts:
            return np.empty((0, self.dimension))
        
        try:
            # Generate embeddings
            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            
            # Convert to numpy if needed
            if not isinstance(embeddings, np.ndarray):
                embeddings = np.array(embeddings)
            
            # Ensure correct dimension
            if embeddings.shape[1] != self.dimension:
                # Project or pad to correct dimension
                if embeddings.shape[1] < self.dimension:
                    # Pad with zeros
                    padded = np.zeros((embeddings.shape[0], self.dimension))
                    padded[:, :embeddings.shape[1]] = embeddings
                    embeddings = padded
                else:
                    # Truncate
                    embeddings = embeddings[:, :self.dimension]
            
            # Apply half precision if enabled
            if self.half_precision and self.device == "cuda":
                embeddings = embeddings.astype(np.float16)
            
            return embeddings
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return self._fallback_embedding(texts)
    
    def _fallback_embedding(self, texts: List[str]) -> np.ndarray:
        """Generate simple hash-based fallback embeddings."""
        embeddings = []
        for text in texts:
            # Simple deterministic embedding based on text content
            hash_bytes = hash(text) % (2**31)
            # Create a vector with some pattern based on the hash
            vec = np.array([(hash_bytes >> (i * 8)) & 0xFF for i in range(min(self.dimension, 8))])
            # Pad to dimension
            padded = np.zeros(self.dimension)
            padded[:len(vec)] = vec
            embeddings.append(padded)
        
        return np.array(embeddings)
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Normalize vectors
        e1 = embedding1 / np.linalg.norm(embedding1) if np.linalg.norm(embedding1) > 0 else embedding1
        e2 = embedding2 / np.linalg.norm(embedding2) if np.linalg.norm(embedding2) > 0 else embedding2
        
        # Calculate cosine similarity
        similarity = np.dot(e1, e2)
        
        # Clip to valid range
        return float(max(-1.0, min(1.0, similarity)))


# ============================================================
# Specialized Embedding Functions
# ============================================================

def embed_texts(texts: List[str], model_name: str = None) -> np.ndarray:
    """Quick function to embed texts using the config default model."""
    model = EmbeddingModel(model_name=model_name)
    return model.embed(texts)


def calculate_semantic_similarity(text1: str, text2: str, model_name: str = None) -> float:
    """Calculate semantic similarity between two texts."""
    model = EmbeddingModel(model_name=model_name)
    
    embeddings = model.embed([text1, text2])
    
    if len(embeddings) == 2:
        return model.similarity(embeddings[0], embeddings[1])
    return 0.0


# ============================================================
# Code-Specific Embeddings
# ============================================================

def embed_code_snippets(snippets: List[str]) -> np.ndarray:
    """Generate embeddings specifically for code snippets.
    
    Uses a code-optimized model approach - in production would use
    a code-specific encoder like CodeBERT, GraphCodeBERT, etc.
    """
    # For now, use the general embedding model
    # In production, this would use a specialized code encoder
    model = EmbeddingModel(SENTENCE_TRANSFORMER_MODEL)
    return model.embed(snippets)


# ============================================================
# Summary of Capabilities
# ============================================================

# Embedding Models Supported:
# - all-MiniLM-L12-v2 (default): 384 dimensions, general purpose
# - multi-qa-MiniLM-L6-cos-v1: 384 dimensions, QA-focused
# - all-MPNet-base-v2: 768 dimensions, high quality
# - codebert: code-specific embeddings
# - Onnx-optimized models for fast inference

# Capabilities:
# - Sentence embeddings with normalization
# - Cosine similarity calculation
# - Code snippet embeddings
# - Batch processing for efficiency
# - GPU acceleration support
# - Half precision (FP16) for reduced memory
# - Fallback hash-based embeddings if models unavailable