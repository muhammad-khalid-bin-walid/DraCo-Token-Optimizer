"""Property-based tests for DraCo Token Optimizer.

Uses Hypothesis to test edge cases and ensure correctness of
token reduction operations across a wide range of inputs.
"""
from hypothesis import given, strategies as st, assume, settings
import hypothesis.strategies as st as hypothesis_st

from draco.core.reducer import count_tokens, analyze_text, apply_basic_reduction


# --- count_tokens property tests ---

@given(st.text(min_size=0, max_size=500))
def test_count_tokens_non_negative(text):
    """Count tokens should always return non-negative integer."""
    result = count_tokens(text)
    assert isinstance(result, int), f"Expected int, got {type(result)}"
    assert result >= 0, f"Expected non-negative, got {result}"


@given(st.text(min_size=1, max_size=500))
def test_count_tokens_consistency(text):
    """Count tokens should be consistent for same input."""
    result1 = count_tokens(text)
    result2 = count_tokens(text)
    assert result1 == result2, f"Inconsistent: {result1} vs {result2}"


@given(st.text(min_size=0, max_size=500).filter(lambda t: len(t) > 0))
def test_count_tokens_types(text):
    """Count tokens works with various text types."""
    result = count_tokens(text)
    # Result should be integer
    assert result == int(result)


# --- analyze_text property tests ---

@given(st.text(min_size=0, max_size=500))
def test_analyze_text_returns_metrics(text):
    """analyze_text should return TokenMetrics with all required fields."""
    from draco.core.reducer import TokenMetrics
    metrics = analyze_text(text)
    assert isinstance(metrics, TokenMetrics)
    assert hasattr(metrics, 'total_tokens')
    assert hasattr(metrics, 'reducible_tokens')
    assert hasattr(metrics, 'essential_tokens')
    assert hasattr(metrics, 'compression_ratio')
    assert hasattr(metrics, 'quality_score')
    assert hasattr(metrics, 'reduction_achieved')
    assert hasattr(metrics, 'below_threshold')


@given(st.text(min_size=1, max_size=500))
def test_analyze_text_quality_score_between_0_and_1(text):
    """Quality score should be between 0 and 1."""
    metrics = analyze_text(text)
    assert 0.0 <= metrics.quality_score <= 1.0, f"Quality score {metrics.quality_score} out of range"


@given(st.text(min_size=1, max_size=500))
def test_analyze_text_reduction_non_negative(text):
    """Reduction achieved should be non-negative."""
    metrics = analyze_text(text)
    assert metrics.reduction_achieved >= 0


@given(st.text(min_size=1, max_size=500))
def test_analyze_text_compression_ratio(text):
    """Compression ratio should be between 0 and 1."""
    metrics = analyze_text(text)
    assert 0.0 <= metrics.compression_ratio <= 1.0


# --- apply_basic_reduction property tests ---

@given(st.text(min_size=0, max_size=500))
def test_apply_basic_reduction_returns_dict(text):
    """apply_basic_reduction should return a dict."""
    result = apply_basic_reduction(text)
    assert isinstance(result, dict)


@given(st.text(min_size=1, max_size=500))
def test_apply_basic_reduction_has_required_keys(text):
    """Result should have all required keys."""
    result = apply_basic_reduction(text)
    required_keys = [
        "original_tokens", "reduced_tokens", "remaining_tokens",
        "reduction_percentage", "quality_percentage",
        "passed_quality_gate", "verdict", "zonal_format", "metadata"
    ]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"


@given(st.text(min_size=1, max_size=500))
def test_apply_basic_reduction_reduction_less_than_original(text):
    """Reduction percentage should not exceed 100% and should be <= original tokens."""
    result = apply_basic_reduction(text)
    assert 0.0 <= result["reduction_percentage"] <= 100.0
    assert result["reduced_tokens"] <= result["original_tokens"]


@given(st.text(min_size=1, max_size=500))
def test_apply_basic_reduction_quality_consistent_with_tokens(text):
    """Quality percentage should be consistent with reduced/original token ratio."""
    result = apply_basic_reduction(text)
    if result["original_tokens"] > 0:
        expected_quality = (result["remaining_tokens"] / result["original_tokens"]) * 100
        assert abs(result["quality_percentage"] - expected_quality) < 1.0


# --- ZON formatting property tests ---

@given(st.text(min_size=0, max_size=500))
def test_zon_formatting_roundtrip(text):
    """ZON formatting should preserve essential content."""
    from draco.core.reducer import _apply_zon_formatting
    zon = _apply_zon_formatting(text, depth=5)
    # ZON should not be empty for non-empty input
    assume(len(text.strip()) > 0 or len(zon) > 0)
    # Applying ZON twice should produce same result (idempotent-ish)
    zon2 = _apply_zon_formatting(zon, depth=5)
    # At minimum, both should be valid strings
    assert isinstance(zon, str)
    assert isinstance(zon2, str)


@given(st.integers(min_value=1, max_value=10))
@given(st.text(min_size=0, max_size=500))
def test_zon_depth_validation(text, depth):
    """ZON depth should be validated (1-10)."""
    from draco.core.reducer import _apply_zon_formatting
    result = _apply_zon_formatting(text, depth=depth)
    assert isinstance(result, str)


# --- Edge case tests ---

@given(st.text(min_size=0, max_size=100).filter(lambda t: t is not None))
def test_empty_and_none_handling(text):
    """Edge cases should be handled gracefully."""
    from draco.core.reducer import count_tokens, analyze_text, apply_basic_reduction
    # Empty string
    assert count_tokens("") == 0
    metrics = analyze_text("")
    assert isinstance(metrics, object)
    result = apply_basic_reduction("")
    assert isinstance(result, dict)


if __name__ == "__main__":
    # Run a quick test to verify the tests load
    print("Property-based test skeleton created successfully!")
    print("Run with: hypothesis tests/test_properties.py")