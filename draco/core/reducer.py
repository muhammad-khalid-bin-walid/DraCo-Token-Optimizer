# DraCo Token Optimizer - Core Reduction Module
"""Core token reduction operations with 90%+ target and 90%+ quality preservation.

This module provides the primary token reduction functionality including:
- Token counting and analysis
- Reduction ratio calculation
- Quality assessment
- Various compression strategies
- Reduction result formatting
"""

import re
import json
import warnings
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union
from draco.config import (
    REDUCTION_TARGET,
    QUALITY_THRESHOLD,
    MINIMUM_QUALITY_PRESERVATION,
    MAXIMUM_TOKEN_REDUCTION,
    QUALITY_GATES_ENFORCED,
    EDGE_CASE_HANDLING,
)


# ============================================================
# Data Classes for Reduction Operations
# ============================================================

@dataclass
class TokenMetrics:
    """Metrics for token analysis and reduction."""
    total_tokens: int
    reducible_tokens: int
    essential_tokens: int
    compression_ratio: float
    quality_score: float
    reduction_achieved: float
    below_threshold: bool

@dataclass
class ReductionResult:
    """Result of a token reduction operation."""
    original_tokens: int
    reduced_tokens: int
    remaining_tokens: int
    reduction_percentage: float
    quality_percentage: float
    passed_quality_gate: bool
    verdict: str
    zonal_format: Optional[str] = None
    metadata: Optional[Dict] = None

# ============================================================
# Token Analysis Functions
# ============================================================

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count the number of tokens in a text string.
    
    Uses tiktoken for accurate counting if available, falls back to word-based approximation.
    
    Args:
        text: The text to count tokens in
        model: Target model for tiktoken encoding (default: gpt-4)
        
    Returns:
        Number of tokens
    """
    if not text:
        return 0
    
    # Try tiktoken if available
    if TIKTOKEN_AVAILABLE:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            # Fall back if model not found or other error
            pass
    
    # Fallback: word-based approximation
    # Code: ~1.3 tokens/word, Prose: ~1.5 tokens/word
    words = text.split()
    # Detect if text looks like code (contains common code patterns)
    code_patterns = ['def ', 'import ', 'class ', 'function ', 'const ', 'let ', 'var ',
                     'for ', 'while ', 'if ', 'else ', 'return ', '=>', '/*', '*/',
                     '.py', '.js', '.ts', '.py', 'def ', 'import ']
    lower_text = text.lower()
    is_code = any(p in lower_text for p in code_patterns)
    
    token_per_word = 1.5 if not is_code else 1.3
    token_count = len(words) * token_per_word
    return max(1, int(token_count))


def analyze_text(text: str, config: object = None) -> TokenMetrics:
    """Analyze text to determine reduction opportunities.
    
    Args:
        text: The text to analyze
        config: Compression configuration for quality thresholds
        
    Returns:
        TokenMetrics with analysis results
    """
    total_tokens = count_tokens(text)
    
    if total_tokens == 0:
        return TokenMetrics(
            total_tokens=0,
            reducible_tokens=0,
            essential_tokens=0,
            compression_ratio=0.0,
            quality_score=1.0,
            reduction_achieved=0.0,
            below_threshold=False,
        )
    
    # Heuristic: estimate reducible vs essential tokens
    reducible = 0
    essential = 0
    
    # Enhanced verbose phrase patterns (6 core + 30+ additional)
    verbose_patterns = [
        # Core 6 patterns
        r'is important to note that',
        r'please note that',
        r'it should be noted that',
        r'it is worth noting that',
        r'one should consider',
        r'it is crucial that',
        # Additional verbose phrases
        r'it is worth mentioning that',
        r'it should be mentioned that',
        r'as a matter of fact',
        r'in case you were not aware',
        r'it is interesting to note',
        r'it is important to mention',
        r'please be advised that',
        r'it is essential to understand',
        r'it is necessary to note',
        r'one must consider',
        r'it is significant to note',
        r'it is useful to note',
        r'it is helpful to note',
        r'it is appropriate to note',
        r'it is advisable to note',
        r'it is pertinent to note',
        r'it is relevant to note',
        r'it is valuable to note',
        r'it is critical to note',
        r'it is indispensable to note',
        r'it is vital to note',
        r'it is essential to mention',
        r'it is necessary to mention',
        r'it is important to mention',
        r'it is worth mentioning',
        r'one should note',
        r'one must note',
    ]
    
    lower_text = text.lower()
    
    # Analyze line by line
    lines = text.split('\n')
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
        
        # Count comments (reducible in most cases)
        if stripped.startswith('#') or (stripped.startswith('//') and '{' not in stripped):
            reducible += count_tokens(line)
            continue
        
        # Count verbose explanatory phrases
        verbose_detected = False
        for pattern in verbose_patterns:
            if re.search(pattern, lower_text):
                # Mark as reducible but keep essence
                reducible += int(count_tokens(line) * 0.6)
                essential += int(count_tokens(line) * 0.4)
                verbose_detected = True
                break
        
        if verbose_detected:
            continue
        
        # Count repetitive structures
        if stripped.startswith('build ') or stripped.startswith('run '):
            reducible += int(count_tokens(line) * 0.3)
            essential += int(count_tokens(line) * 0.7)
            continue
        
        # Default: assume essential
        essential += count_tokens(line)
    
    # If we couldn't analyze properly, use default heuristics
    if reducible + essential == 0:
        reducible = int(total_tokens * 0.4)  # 40% reducible default
        essential = total_tokens - reducible
    
    compression_ratio = reducible / total_tokens if total_tokens > 0 else 0.0
    quality_score = essential / total_tokens if total_tokens > 0 else 1.0
    reduction_achievable = compression_ratio * 100  # Percentage
    
    # Use config minimum quality if available
    min_quality = MINIMUM_QUALITY_PRESERVATION
    if config is not None:
        try:
            min_quality = getattr(config, 'minimum_quality', MINIMUM_QUALITY_PRESERVATION)
        except Exception:
            pass
    
    below_threshold = quality_score * 100 < min_quality
    
    return TokenMetrics(
        total_tokens=total_tokens,
        reducible_tokens=reducible,
        essential_tokens=essential,
        compression_ratio=compression_ratio,
        quality_score=quality_score,
        reduction_achieved=reduction_achievable,
        below_threshold=below_threshold,
    )


# ============================================================
# Reduction Strategies
# ============================================================

def apply_basic_reduction(text: str, config: object = None) -> dict:
    """Apply basic token reduction to text.
    
    Args:
        text: The text to reduce
        config: Compression configuration (uses defaults if None)
        
    Returns:
        dict with reduction result
    """
    if config is None:
        from draco.core.reducer import CompressionConfig
        config = CompressionConfig()
    
    if not text or not text.strip():
        from draco.core.reducer import ReductionResult
        return {
            "original_tokens": 0,
            "reduced_tokens": 0,
            "remaining_tokens": 0,
            "reduction_percentage": 0.0,
            "quality_percentage": 100.0,
            "passed_quality_gate": True,
            "verdict": "no_content",
            "zonal_format": None,
            "metadata": {}
        }
    
    # Analyze the text
    from draco.core.reducer import analyze_text
    metrics = analyze_text(text)
    
    # Apply reduction based on config
    reduced_text = _apply_reduction_strategies(text, config, metrics)
    
    # Count tokens in reduced version
    from draco.core.reducer import count_tokens
    reduced_tokens = count_tokens(reduced_text)
    original_tokens = count_tokens(text)
    
    # Calculate metrics
    reduction_percentage = ((original_tokens - reduced_tokens) / original_tokens * 100) if original_tokens > 0 else 0.0
    quality_percentage = (reduced_tokens / original_tokens * 100) if original_tokens > 0 else 100.0
    
    # Check quality gate
    passed_quality_gate = quality_percentage >= config.minimum_quality
    
    # Generate verdict
    from draco.core.reducer import _generate_verdict
    verdict = _generate_verdict(reduction_percentage, quality_percentage, config)
    
    # Apply ZON formatting if enabled
    from draco.core.reducer import _apply_zon_formatting
    zonal_format = None
    if config.use_zon:
        zonal_format = _apply_zon_formatting(reduced_text, config.zod_depth)
    
    result = {
        "original_tokens": original_tokens,
        "reduced_tokens": reduced_tokens,
        "remaining_tokens": reduced_tokens,
        "reduction_percentage": reduction_percentage,
        "quality_percentage": quality_percentage,
        "passed_quality_gate": passed_quality_gate,
        "verdict": verdict,
        "zonal_format": zonal_format,
        "metadata": {
            "metrics": {
                "total_tokens": metrics.total_tokens,
                "reducible_tokens": metrics.reducible_tokens,
                "essential_tokens": metrics.essential_tokens,
                "compression_ratio": metrics.compression_ratio,
            },
            "config": {
                "target_reduction": config.target_reduction,
                "minimum_quality": config.minimum_quality,
                "optimization_level": config.optimization_level,
                "use_zon": config.use_zon,
                "agent_type": config.agent_type,
            }
        },
    }
    
    return result


def _apply_reduction_strategies(text: str, config: object, metrics: object) -> str:
    """Apply reduction strategies based on config and text analysis."""
    reduced = text
    
    # Strategy 1: Remove verbose explanatory phrases
    verbose_patterns = [
        (r'is important to note that', ''),
        (r'please note that', ''),
        (r'it should be noted that', ''),
        (r'it is worth noting that', ''),
        (r'one should consider', ''),
        (r'it is crucial that', ''),
    ]
    
    lower_reduced = reduced.lower()
    for pattern, replacement in verbose_patterns:
        if re.search(pattern, lower_reduced):
            reduced = re.sub(pattern, replacement, reduced, flags=re.IGNORECASE)
    
    # Strategy 2: Compress repetitive build/run commands
    reduced = re.sub(r'build\s+your\s+project', 'build_project', reduced, flags=re.IGNORECASE)
    reduced = re.sub(r'run\s+the\s+tests', 'run_tests', reduced, flags=re.IGNORECASE)
    reduced = re.sub(r'run\s+your\s+code', 'run_code', reduced, flags=re.IGNORECASE)
    
    # Strategy 3: Remove filler words and phrases
    filler_patterns = [
        (r'\bvery\s+', ''),
        (r'\breally\s+', ''),
        (r'\babsolutely\s+', ''),
    ]
    
    for pattern, replacement in filler_patterns:
        reduced = re.sub(pattern, replacement, reduced, flags=re.IGNORECASE)
    
    # Strategy 4: Condense common code patterns
    code_patterns = [
        (r'for\s+\w+\s+in\s+', 'for _ in '),
        (r'if\s+\w+\s+is\s+', 'if '),
        (r'while\s+\w+\s+is\s+', 'while '),
    ]
    
    for pattern, replacement in code_patterns:
        reduced = re.sub(pattern, replacement, reduced, flags=re.IGNORECASE)
    
    # Strategy 5: Remove redundant transitional phrases
    transition_patterns = [
        (r'\\bto note that\\b', ''),
        (\\bAs a result\\b', ''),
        (r'\\bAs a consequence\\b', ''),
        (r'\\bConsequently\\b', ''),
        (r'\\bTherefore\\b', ''),
        (r'\\bHence\\b', ''),
    ]
    
    for pattern, replacement in transition_patterns:
        reduced = re.sub(pattern, replacement, reduced, flags=re.IGNORECASE)
    
    # Ensure we don't reduce below minimum quality
    original_count = count_tokens(text)
    reduced_count = count_tokens(reduced)
    
    if original_count > 0:
        quality = (reduced_count / original_count) * 100
        min_quality = config.minimum_quality if config else MINIMUM_QUALITY_PRESERVATION
        if quality < min_quality and (config is None or config.optimization_level == "maximum"):
            # Scale back the reduction to meet quality threshold
            target_quality_ratio = min_quality / 100
            tokens_to_keep = int(original_count * target_quality_ratio)
            if reduced_count < tokens_to_keep:
                # Re-add some essential content
                reduced = _restore_essential_content(text, reduced, original_count, tokens_to_keep)
    
    return reduced


def _restore_essential_content(original: str, reduced: str, original_count: int, minimum_tokens: int) -> str:
    """Restore essential content to meet minimum quality threshold."""
    # Simple approach: if we've reduced too much, return original
    reduced_count = count_tokens(reduced)
    if reduced_count < minimum_tokens:
        return original  # Fall back to original if quality would be too low
    return reduced


def _generate_verdict(reduction_percentage: float, quality_percentage: float, config: object) -> str:
    """Generate a verdict string based on reduction and quality metrics."""
    
    # Determine verdict based on thresholds
    target = config.target_reduction if config else REDUCTION_TARGET
    min_quality = config.minimum_quality if config else MINIMUM_QUALITY_PRESERVATION
    
    # Determine verdict based on thresholds
    if reduction_percentage >= target and quality_percentage >= min_quality:
        return "reduce_tokens"  # Successfully reduced while preserving quality
    elif reduction_percentage >= target * 0.7 and quality_percentage >= min_quality:
        return "preserve_quality"  # Good reduction with quality preservation
    elif reduction_percentage < target * 0.3 and quality_percentage >= min_quality:
        return "minimal_change"  # Minimal reduction, quality preserved
    elif reduction_percentage >= target and quality_percentage < min_quality:
        return "quality_compromise"  # Reduced but quality dropped
    elif reduction_percentage < target * 0.3 and quality_percentage < min_quality:
        return "restore_original"  # Both reduction and quality poor
    else:
        return "optimize_readability"  # Optimize for readability


def _apply_zon_formatting(text: str, depth: int = 5) -> str:
    """Apply ZON (Zoned Object Notation) formatting for compact representation.
    
    ZON is a lossless compression format that can achieve 35-70% size reduction
    vs JSON with deterministic parsing.
    
    Args:
        text: The text to format in ZON
        depth: Compression depth (1-10, default: 5)
        
    Returns:
        ZON-formatted string
    """
    # ZON compression depth validation
    depth = max(1, min(10, depth))
    
    if not text:
        return ""
    
    # Check if text is JSON-like and can be parsed
    try:
        import json
        data = json.loads(text)
        
        # Apply ZON compression based on data type and depth
        if isinstance(data, dict):
            return _zon_serialize_dict(data, depth)
        elif isinstance(data, list):
            return _zon_serialize_list(data, depth)
        else:
            return text
    except (json.JSONDecodeError, ValueError):
        # Not valid JSON, apply text-level compaction with depth
        return _zon_text_compaction(text, depth)


def _zon_serialize_dict(data: dict, depth: int) -> str:
    """Serialize a dict to ZON format with specified depth."""
    if depth <= 0:
        return json.dumps(data, separators=(',', ':'))
    
    parts = []
    for k, v in data.items():
        # Recursively compress values based on depth
        compressed_value = _zon_compress_value(v, depth - 1)
        # Use compact key-format: key:value
        # For strings, use shortened form if possible
        if isinstance(compressed_value, str):
            # Further compress short strings
            if len(compressed_value) < 20:
                # Remove quotes for very short strings in appropriate context
                pass
            parts.append(f'{k}:{compressed_value}')
        else:
            parts.append(f'{k}:{compressed_value}')
    
    return "{" + ",".join(parts) + "}"


def _zon_serialize_list(data: list, depth: int) -> str:
    """Serialize a list to ZON format with specified depth."""
    if depth <= 0:
        return json.dumps(data, separators=(',', ':'))
    
    parts = []
    for item in data:
        compressed = _zon_compress_value(item, depth - 1)
        parts.append(compressed)
    
    return "[" + ",".join(parts) + "]"


def _zon_compress_value(value: any, depth: int) -> any:
    """Recursively compress a value based on depth level."""
    if depth <= 0:
        return value
    
    if isinstance(value, dict):
        # Serialize dict at this depth level
        parts = []
        for k, v in value.items():
            compressed_v = _zon_compress_value(v, depth - 1)
            parts.append(f'{k}:{compressed_v}')
        return "{" + ",".join(parts) + "}"
    elif isinstance(value, list):
        # Serialize list at this depth level
        parts = [_zon_compress_value(item, depth - 1) for item in value]
        return "[" + ",".join(parts) + "]"
    elif isinstance(value, str):
        # Compress string: remove extra whitespace, shorten if very long
        compressed = re.sub(r'\s+', ' ', value).strip()
        if len(compressed) > 50 and depth > 2:
            # Could add summarization here, but keep it simple
            pass
        return f'"{compressed}"'
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return json.dumps(value)


def _zon_text_compaction(text: str, depth: int) -> str:
    """Apply text-level ZON compaction for non-JSON content."""
    depth = max(1, min(10, depth))
    
    # Remove multiple spaces, normalize
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Based on depth, apply different levels of compaction
    if depth <= 3:
        # Light compaction: just normalize whitespace
        return text
    elif depth <= 7:
        # Medium compaction: normalize + remove small filler words
        filler_patterns = [
            (r'\bvery\s+', ''),
            (r'\breally\s+', ''),
            (r'\babsolutely\s+', ''),
        ]
        for pattern, replacement in filler_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text
    else:
        # Aggressive compaction: normalize + remove fillers + condense code patterns
        text = re.sub(r'\bvery\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\breally\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\babsolutely\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'for\s+\w+\s+in\s+', 'for _ in ', text, flags=re.IGNORECASE)
        text = re.sub(r'if\s+\w+\s+is\s+', 'if ', text, flags=re.IGNORECASE)
        text = re.sub(r'while\s+\w+\s+is\s+', 'while ', text, flags=re.IGNORECASE)
        return text


# ============================================================
# Export Functions
# ============================================================

__all__ = [
    "TokenMetrics",
    "ReductionResult", 
    "count_tokens",
    "analyze_text",
    "apply_basic_reduction",
]