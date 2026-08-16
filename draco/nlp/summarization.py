# DraCo Token Optimizer - NLP Summarization Module
"""Abstractive and extractive summarization using transformer models.

Provides summarization with PEGASUS and BART models, sentence extraction,
and quality assessment for token reduction workflows.
"""

import re
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from draco.config import (
    PEGASUS_MODEL_NAME,
    BART_MODEL_NAME,
    SUMMARIZATION_RATIO,
    GENERATION_TEMPERATURE,
    DEVICE,
    USE_GPU_ACCELERATION,
    USE_HALF_PRECISION,
    VERDICT_TASK_TYPE,
)


# ============================================================
# Summarization Result Data Class
# ============================================================

@dataclass
class SummarizationResult:
    """Result of a summarization operation."""
    original_text: str
    summary: str
    original_tokens: int
    summary_tokens: int
    compression_ratio: float
    quality_score: float
    verdict: str
    model_used: str
    extraction_ratio: float


# ============================================================
# Summarizer Base Class
# ============================================================

class Summarizer:
    """Base class for summarization models."""
    
    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or PEGASUS_MODEL_NAME
        self.device = device or DEVICE
        self.half_precision = USE_HALF_PRECISION
        self.model = None
        self._loaded = False
    
    def _ensure_loaded(self):
        """Load the model if not already loaded."""
        if self._loaded:
            return
        
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            
            model_kwargs = {}
            if self.half_precision and self.device == "cuda":
                model_kwargs["torch_dtype"] = "float16"
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, **model_kwargs)
            self.model.to(self.device)
            self.model.eval()
            
            self._loaded = True
            print(f"Summarizer model loaded: {self.model_name}")
            
        except ImportError:
            print("transformers not available, using extractive fallback")
            self._loaded = True
        except Exception as e:
            print(f"Error loading summarizer: {e}")
            self._loaded = True
    
    def summarize(self, text: str, ratio: float = None) -> str:
        """Generate a summary of the text.
        
        Args:
            text: The text to summarize
            ratio: Summary ratio (0.0 to 1.0, defaults to config SUMMARIZATION_RATIO)
            
        Returns:
            Summary text
        """
        if ratio is None:
            ratio = SUMMARIZATION_RATIO
        
        if not text or not text.strip():
            return ""
        
        self._ensure_loaded()
        
        if not self.model:
            return self._extractive_summarize(text, ratio)
        
        try:
            return self._abstractive_summarize(text, ratio)
        except Exception as e:
            print(f"Abstractive summarization failed: {e}, falling back to extractive")
            return self._extractive_summarize(text, ratio)
    
    def _extractive_summarize(self, text: str, ratio: float) -> str:
        """Extractive summarization by selecting important sentences."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return text
        
        # Calculate importance based on keyword density and position
        # Important keywords for code/technical content
        important_keywords = [
            'import', 'from', 'class', 'def', 'return', 'function', 'method',
            'configuration', 'setting', 'parameter', 'option', 'config',
            'reduce', 'token', 'compression', 'quality', 'preservation',
        ]
        
        # Score each sentence
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = 0
            lower_sentence = sentence.lower()
            
            # Keyword match score
            for kw in important_keywords:
                if kw in lower_sentence:
                    score += 1
            
            # Position bias: earlier sentences are more important
            position_score = max(0, 1 - (i / len(sentences)) * 0.5)
            score += position_score
            
            # Length normalization: prefer medium-length sentences
            length_score = 1.0 - abs(len(sentence.split()) - 10) / 20
            score *= max(0.1, length_score)
            
            scored_sentences.append((score, sentence))
        
        # Sort by score and select top ratio
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        
        # Select sentences maintaining original order
        num_to_select = max(1, int(len(sentences) * ratio))
        selected_indices = set()
        for score, sentence in scored_sentences[:num_to_select]:
            # Find the sentence in original order
            for i, s in enumerate(sentences):
                if s.strip() == sentence.strip() and i not in selected_indices:
                    selected_indices.add(i)
                    break
        
        # Return selected sentences in original order
        selected_indices = sorted(selected_indices)
        summary_sentences = [sentences[i] for i in selected_indices]
        
        return ' '.join(summary_sentences)
    
    def _abstractive_summarize(self, text: str, ratio: float) -> str:
        """Abstractive summarization using the transformer model."""
        if not self.model:
            return self._extractive_summarize(text, ratio)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                max_length=512,
                truncation=True,
                return_tensors="pt",
            ).to(self.device)
            
            # Calculate target summary length based on ratio
            original_length = len(text.split())
            target_length = max(1, int(original_length * ratio))
            target_length = max(target_length, 5)  # Minimum 5 tokens
            target_length = min(target_length, 150)  # Maximum 150 tokens
            
            # Generate summary using model
            with torch_no_grad():
                summary_ids = self.model.generate(
                    **inputs,
                    max_length=target_length,
                    num_beams=4,
                    temperature=GENERATION_TEMPERATURE,
                    do_sample=True,
                    early_stopping=True,
                )
            
            # Decode summary
            summary = self.tokenizer.decode(
                summary_ids[0], 
                skip_special_tokens=True,
            )
            
            return summary
            
        except Exception as e:
            print(f"Abstractive summarization error: {e}")
            return self._extractive_summarize(text, ratio)


# ============================================================
# Global Summarizer Instances
# ============================================================

# PEGASUS summarizer for verdict generation
_pegasus_summarizer = None

def get_pegasus_summarizer() -> Summarizer:
    """Get the PEGASUS summarizer instance (lazy loaded)."""
    global _pegasus_summarizer
    if _pegasus_summarizer is None:
        _pegasus_summarizer = Summarizer(model_name=PEGASUS_MODEL_NAME)
    return _pegasus_summarizer

# BART summarizer for alternative summarization
_bart_summarizer = None

def get_bart_summarizer() -> Summarizer:
    """Get the BART summarizer instance (lazy loaded)."""
    global _bart_summarizer
    if _bart_summarizer is None:
        _bart_summarizer = Summarizer(model_name=BART_MODEL_NAME)
    return _bart_summarizer


# ============================================================
# Quick Summary Function
# ============================================================

def summarize_text(text: str, model: str = "pegasus", ratio: float = None) -> str:
    """Quick function to summarize text.
    
    Args:
        text: The text to summarize
        model: Which model to use ("pegasus" or "bart")
        ratio: Summary ratio (0.0-1.0, defaults to config)
        
    Returns:
        Summary text
    """
    if ratio is None:
        ratio = SUMMARIZATION_RATIO
    
    if model == "pegasus":
        summarizer = get_pegasus_summarizer()
    elif model == "bart":
        summarizer = get_bart_summarizer()
    else:
        summarizer = get_pegasus_summarizer()
    
    return summarizer.summarize(text, ratio)


# ============================================================
# Summarization with Quality Assessment
# ============================================================

def summarize_with_assessment(
    text: str, 
    ratio: float = None,
    preserve_verdict: str = None
) -> SummarizationResult:
    """Summarize text and assess quality for token reduction workflows.
    
    Args:
        text: The text to summarize
        ratio: Summary ratio
        preserve_verdict: If provided, use this verdict instead of auto-detecting
        
    Returns:
        SummarizationResult with quality metrics and verdict
    """
    if ratio is None:
        ratio = SUMMARIZATION_RATIO
    
    if not text or not text.strip():
        return SummarizationResult(
            original_text=text or "",
            summary="",
            original_tokens=0,
            summary_tokens=0,
            compression_ratio=0.0,
            quality_score=1.0,
            verdict="no_content" if not preserve_verdict else preserve_verdict,
            model_used="none",
            extraction_ratio=0.0,
        )
    
    # Generate summary
    summary = summarize_text(text, model="pegasus", ratio=ratio)
    
    # Count tokens
    original_tokens = count_tokens(text)
    summary_tokens = count_tokens(summary)
    
    # Calculate compression ratio
    compression_ratio = summary_tokens / original_tokens if original_tokens > 0 else 1.0
    
    # Calculate quality score based on information preservation
    # Simple heuristic: ratio closer to optimal is better quality
    # Optimal ratio for technical content is typically 0.3-0.5
    optimal_ratio = 0.4
    ratio_deviation = abs(ratio - optimal_ratio)
    quality_base = max(0, 100 - (ratio_deviation * 100))
    
    # Additional quality check: ensure essential content is preserved
    # Check for key technical terms
    key_terms = _extract_key_terms(text)
    preserved_terms = _count_preserved_terms(key_terms, summary)
    term_quality = (preserved_terms / len(key_terms) * 100) if key_terms else 100.0
    
    # Combine quality scores
    quality_score = round((quality_base * 0.6 + term_quality * 0.4), 2)
    
    # Determine verdict
    if preserve_verdict:
        verdict = preserve_verdict
    elif ratio >= 0.5:
        verdict = "minimal_change"
    elif compression_ratio < 0.2 and quality_score > 80:
        verdict = "quality_compromise"  # Too aggressive, quality at risk
    elif compression_ratio >= 0.3 and quality_score >= 80:
        verdict = "reduce_tokens"  # Good reduction with quality preservation
    elif compression_ratio >= 0.2 and quality_score >= 70:
        verdict = "preserve_quality"  # Moderate reduction, quality okay
    else:
        verdict = "restore_original"  # Too aggressive or poor quality
    
    return SummarizationResult(
        original_text=text,
        summary=summary,
        original_tokens=original_tokens,
        summary_tokens=summary_tokens,
        compression_ratio=compression_ratio,
        quality_score=quality_score,
        verdict=verdict,
        model_used="pegasus",
        extraction_ratio=ratio,
    )


def _extract_key_terms(text: str) -> List[str]:
    """Extract key technical terms from text."""
    # Important technical keywords to preserve
    terms = []
    
    # Common technical terms in code/technical docs
    tech_terms = [
        'import', 'from', 'class', 'def', 'return', 'function', 'method',
        'configuration', 'setting', 'parameter', 'option',
        'reduce', 'token', 'compression', 'quality', 'preservation',
        'PEGASUS', 'BART', 'transformer', 'embedding',
    ]
    
    lower_text = text.lower()
    for term in tech_terms:
        if term.lower() in lower_text:
            terms.append(term)
    
    # Also add capitalized words that look like technical terms
    # (words with 4+ chars that appear capitalized)
    import re
    capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
    for word in capitalized:
        if len(word) >= 4 and word not in [t.lower() for t in terms]:
            terms.append(word)
    
    return list(set(terms))  # Remove duplicates


def _count_preserved_terms(key_terms: List[str], summary: str) -> int:
    """Count how many key terms are preserved in the summary."""
    if not key_terms or not summary:
        return 0
    
    summary_lower = summary.lower()
    preserved = 0
    for term in key_terms:
        if term.lower() in summary_lower:
            preserved += 1
    
    return preserved


# ============================================================
# Export Functions
# ============================================================

__all__ = [
    "SummarizationResult",
    "Summarizer",
    "get_pegasus_summarizer",
    "get_bart_summarizer",
    "summarize_text",
    "summarize_with_assessment",
    "_extract_key_terms",
    "_count_preserved_terms",
]