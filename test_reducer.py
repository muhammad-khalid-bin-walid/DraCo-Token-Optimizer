import sys
sys.path.insert(0, 'draco-token-optimizer')

from draco.core.reducer import count_tokens, analyze_text, apply_basic_reduction, TokenMetrics, ReductionResult
print('Core reducer imports OK')

# Test count_tokens
print(f'count_tokens("hello world"): {count_tokens("hello world")}')

# Test analyze_text
text = '# This is a comment\n# Please note that this is a test\ndef hello():\n    pass'
metrics = analyze_text(text)
print(f'analyze_text: total={metrics.total_tokens}, reducible={metrics.reducible_tokens}, essential={metrics.essential_tokens}, quality={metrics.quality_score:.2f}')

# Test apply_basic_reduction
result = apply_basic_reduction(text)
print(f'apply_basic_reduction: reduction={result["reduction_percentage"]:.1f}%, quality={result["quality_percentage"]:.1f}%, verdict={result["verdict"]}')