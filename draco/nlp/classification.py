# DraCo Token Optimizer - NLP Classification Module
"""Text classification and intent detection for token optimization workflows.

Provides intent classification, importance scoring, and quality assessment
using BERT-based and other classification models.
"""

import re
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
import numpy as np
from draco.config import (
    BERT_MODEL_NAME,
    IMPORTANCE_THRESHOLD,
    QUALITY_CLASSIFIER_THRESHOLD,
    DEVICE,
    USE_GPU_ACCELERATION,
    USE_HALF_PRECISION,
)


# ============================================================
# Classification Result Data Class
# ============================================================

@dataclass
class ClassificationResult:
    """Result of a text classification operation."""
    text: str
    predicted_class: str
    confidence: float
    all_scores: Dict[str, float]
    importance_score: float
    quality_score: float
    verdict: str
    model_used: str


# ============================================================
# Classifier Base Class
# ============================================================

class TextClassifier:
    """Base class for text classification models."""
    
    def __init__(self, model_name: str = None, device: str = None):
        self.model_name = model_name or BERT_MODEL_NAME
        self.device = device or DEVICE
        self.half_precision = USE_HALF_PRECISION
        self.model = None
        self.tokenizer = None
        self._loaded = False
        self.num_classes = 3  # Default: low, medium, high
    
    def _ensure_loaded(self):
        """Load the model if not already loaded."""
        if self._loaded:
            return
        
        try:
            from transformers import BertForSequenceClassification, BertTokenizer
            
            self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
            self.model = BertForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            
            # Get number of classes from model config
            self.num_classes = self.model.config.num_labels
            
            self._loaded = True
            print(f"Classifier loaded: {self.model_name}, classes: {self.num_classes}")
            
        except ImportError:
            print("transformers not available, using rule-based fallback")
            self._loaded = True
        except Exception as e:
            print(f"Error loading classifier: {e}")
            # Use rule-based fallback
            self._loaded = True
    
    def classify(self, text: str) -> ClassificationResult:
        """Classify the input text.
        
        Args:
            text: The text to classify
            
        Returns:
            ClassificationResult with predicted class and scores
        """
        if not text or not text.strip():
            return ClassificationResult(
                text=text or "",
                predicted_class="neutral",
                confidence=1.0,
                all_scores={"neutral": 1.0},
                importance_score=0.0,
                quality_score=1.0,
                verdict="no_content",
                model_used=self.model_name or "rule-based",
            )
        
        self._ensure_loaded()
        
        if not self.model:
            return self._rule_based_classify(text)
        
        try:
            return self._model_based_classify(text)
        except Exception as e:
            print(f"Model-based classification failed: {e}, falling back to rule-based")
            return self._rule_based_classify(text)
    
    def _model_based_classify(self, text: str) -> ClassificationResult:
        """Classify using the BERT model."""
        if not self.model or not self.tokenizer:
            return self._rule_based_classify(text)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                max_length=512,
                truncation=True,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            
            # Run inference
            with torch_no_grad():
                outputs = self.model(**inputs)
            
            # Get logits and probabilities
            logits = outputs.logits
            probabilities = torch_no_softmax(logits[0])
            
            # Get predicted class
            predicted_idx = int(torch_no_argmax(logits[0]))
            
            # Convert index to class name
            class_names = self._get_class_names()
            predicted_class = class_names[predicted_idx] if predicted_idx < len(class_names) else f"class_{predicted_idx}"
            
            # Get confidence
            confidence = float(probabilities[predicted_idx])
            
            # Convert all probabilities to dict
            all_scores = {}
            for i, prob in enumerate(probabilities):
                class_name = class_names[i] if i < len(class_names) else f"class_{i}"
                all_scores[class_name] = round(float(prob), 4)
            
            # Calculate importance and quality scores
            importance_score = self._calculate_importance(text, all_scores)
            quality_score = self._calculate_quality(text, all_scores)
            
            # Determine verdict
            verdict = self._determine_verdict(all_scores, importance_score, quality_score)
            
            return ClassificationResult(
                text=text,
                predicted_class=predicted_class,
                confidence=confidence,
                all_scores=all_scores,
                importance_score=importance_score,
                quality_score=quality_score,
                verdict=verdict,
                model_used=self.model_name,
            )
            
        except Exception as e:
            print(f"Classification error: {e}")
            return self._rule_based_classify(text)
    
    def _rule_based_classify(self, text: str) -> ClassificationResult:
        """Classify text using rule-based heuristics."""
        lower_text = text.lower()
        
        # Importance classifier patterns
        importance_patterns = {
            "high": [
                r'\b(reduce|optimize|compress|minimize)\b',
                r'\b(90%|80%|70%)\b',
                r'\b(critical|essential|key)\b',
            ],
            "medium": [
                r'\b(important|significant|notable)\b',
                r'\b(moderately|partially)\b',
            ],
            "low": [
                r'\b(unimportant|trivial|minor)\b',
                r'\b(optional|unnecessary)\b',
            ],
        }
        
        # Quality classifier patterns
        quality_patterns = {
            "high": [
                r'\b(precise|exact|accurate)\b',
                r'\b(verified|validated|confirmed)\b',
            ],
            "medium": [
                r'\b(approximately|roughly|estimated)\b',
            ],
            "low": [
                r'\b(unclear|approximate|guess)\b',
            ],
        }
        
        # Score importance
        importance_score = 0.0
        for level, patterns in importance_patterns.items():
            for pattern in patterns:
                if re.search(pattern, lower_text):
                    # Level priority: high=0.9, medium=0.5, low=0.1
                    priority = {"high": 0.9, "medium": 0.5, "low": 0.1}[level]
                    importance_score = max(importance_score, priority)
        
        # Ensure minimum importance
        if importance_score == 0:
            importance_score = 0.3  # Default medium importance
        
        # Score quality
        quality_score = 0.0
        for level, patterns in quality_patterns.items():
            for pattern in patterns:
                if re.search(pattern, lower_text):
                    priority = {"high": 0.9, "medium": 0.5, "low": 0.1}[level]
                    quality_score = max(quality_score, priority)
        
        # Ensure minimum quality
        if quality_score == 0:
            quality_score = 0.7  # Default good quality
        
        # Determine predicted class
        if importance_score >= 0.7:
            predicted_class = "high"
        elif importance_score >= 0.3:
            predicted_class = "medium"
        else:
            predicted_class = "low"
        
        # Confidence based on how clear the patterns are
        confidence = importance_score  # Use importance as confidence proxy
        
        # All scores dict
        all_scores = {
            "high": round(importance_score, 4),
            "medium": round(max(importance_score - 0.2, 0.1), 4),
            "low": round(max(importance_score - 0.4, 0.01), 4),
        }
        
        # Verdict determination
        verdict = self._determine_verdict_from_importance(importance_score, quality_score)
        
        return ClassificationResult(
            text=text,
            predicted_class=predicted_class,
            confidence=round(confidence, 4),
            all_scores=all_scores,
            importance_score=round(importance_score, 4),
            quality_score=round(quality_score, 4),
            verdict=verdict,
            model_used="rule-based",
        )
    
    def _get_class_names(self) -> List[str]:
        """Get class names from the model configuration."""
        # Default class names
        default_names = ["low", "medium", "high"]
        
        if not self.model:
            return default_names
        
        try:
            # Try to get from model config
            return [f"class_{i}" for i in range(self.num_classes)]
        except:
            return default_names
    
    def _calculate_importance(self, text: str, scores: Dict[str, float]) -> float:
        """Calculate importance score from classification results."""
        # Use the "high" class score as importance indicator
        return scores.get("high", 0.3)
    
    def _calculate_quality(self, text: str, scores: Dict[str, float]) -> float:
        """Calculate quality score from classification results."""
        # Use the "high" quality score
        return scores.get("high", 0.7)
    
    def _determine_verdict(self, scores: Dict[str, float], importance: float, quality: float) -> str:
        """Determine verdict based on classification scores."""
        # Use configured thresholds
        imp_threshold = IMPORTANCE_THRESHOLD
        qual_threshold = QUALITY_CLASSIFIER_THRESHOLD
        
        predicted_class = max(scores, key=scores.get) if scores else "medium"
        
        # Verdict determination
        if predicted_class == "high" and importance >= imp_threshold and quality >= qual_threshold:
            return "reduce_tokens"  # High importance, good quality - can reduce
        elif predicted_class == "medium" and quality >= qual_threshold:
            return "preserve_quality"  # Medium importance, quality okay
        elif predicted_class == "low" or quality < qual_threshold:
            return "minimal_change"  # Low importance or poor quality - be conservative
        elif importance >= imp_threshold and quality < qual_threshold:
            return "quality_compromise"  # Important but quality poor
        else:
            return "optimize_readability"  # Optimize for readability
    
    def _determine_verdict_from_importance(self, importance: float, quality: float) -> str:
        """Determine verdict from importance and quality scores (rule-based)."""
        imp_threshold = IMPORTANCE_THRESHOLD
        qual_threshold = QUALITY_CLASSIFIER_THRESHOLD
        
        if importance >= imp_threshold and quality >= qual_threshold:
            return "reduce_tokens"
        elif importance < imp_threshold and quality >= qual_threshold:
            return "preserve_quality"
        elif quality < qual_threshold:
            return "minimal_change"
        else:
            return "optimize_readability"


# ============================================================
# Global Classifier Instance
# ============================================================

_text_classifier = None

def get_classifier() -> TextClassifier:
    """Get the text classifier instance (lazy loaded)."""
    global _text_classifier
    if _text_classifier is None:
        _text_classifier = TextClassifier(model_name=BERT_MODEL_NAME)
    return _text_classifier


# ============================================================
# Quick Classification Function
# ============================================================

def classify_text(text: str, model: str = "bert") -> ClassificationResult:
    """Quick function to classify text.
    
    Args:
        text: The text to classify
        model: Which model to use ("bert" for rule-based, or other)
        
    Returns:
        ClassificationResult with class and scores
    """
    classifier = get_classifier()
    return classifier.classify(text)


# ============================================================
# Batch Classification
# ============================================================

def classify_batch(texts: List[str]) -> List[ClassificationResult]:
    """Classify a batch of texts."""
    classifier = get_classifier()
    return [classifier.classify(text) for text in texts]


# ============================================================
# Intent Detection
# ============================================================

def detect_intent(text: str) -> str:
    """Detect the primary intent of the text for token optimization.
    
    Returns one of: reduce_tokens, preserve_quality, minimal_change,
    quality_compromise, optimize_readability
    """
    classifier = classify_text(text)
    return classifier.verdict


# ============================================================
# Export Functions
# ============================================================

__all__ = [
    "ClassificationResult",
    "TextClassifier",
    "get_classifier",
    "classify_text",
    "classify_batch",
    "detect_intent",
    "_rule_based_classify",
    "_model_based_classify",
    "_get_class_names",
    "_calculate_importance",
    "_calculate_quality",
    "_determine_verdict",
    "_determine_verdict_from_importance",
]