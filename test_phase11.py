import sys
import os

# Add draco package to path
sys.path.insert(0, 'draco-token-optimizer')
sys.path.insert(0, os.path.dirname(os.path.dirname('draco-token-optimizer')))

# Test imports work
from draco.config import get_reduction_target, get_quality_threshold
from draco.core.reducer import analyze_text, apply_basic_reduction, count_tokens
from draco.metrics import MetricsTracker

print("All imports successful")

# Test basic functionality
reduction = get_reduction_target()
quality = get_quality_threshold()
print(f"Reduction: {reduction}%, Quality: {quality}%")

# Test analysis
metrics = analyze_text("This is a test sentence with some repetitive phrases.")
print(f"Analysis: reducible={metrics.reducible_tokens}, essential={metrics.essential_tokens}, quality={metrics.quality_score}")

# Test reduction
result = apply_basic_reduction("Build your project now.")
print(f"Reduction: {result['reduction_percentage']}%, Quality: {result['quality_percentage']}%, Verdict: {result['verdict']}")

# Test degradation detection
tracker = MetricsTracker()
tracker.record_quality_metrics(type('Q', (), {
    'quality_score': 0.92, 
    'reduced_tokens': 92, 
    'original_tokens': 100, 
    'reduction_achieved': 92.0
})())
tracker.record_operation(type('O', (), {
    'passed_quality_gate': True,
    'metadata': {'original_tokens': 100, 'reduced_tokens': 92}
})())
degradation = tracker.check_degradation(threshold=0.85)
print(f"Degradation detected: {degradation['degradation_detected']}")
print(f"Quality ratio: {degradation['degradation_ratio']}")

# Test self-healing trigger
tracker.record_quality_metrics(type('Q', (), {
    'quality_score': 0.78,
    'reduced_tokens': 78,
    'original_tokens': 100,
    'reduction_achieved': 78.0
})())
tracker.record_operation(type('O', (), {
    'passed_quality_gate': False,
    'metadata': {'original_tokens': 100, 'reduced_tokens': 78}
})())
degradation = tracker.check_degradation(threshold=0.85)
print(f"After degradation: detected={degradation['degradation_detected']}, action={degradation['action_required']}")

# Test agent gates
from draco._ import get_yagni_level, get_agent_profile
profile = get_agent_profile("claude_code")
yagni = get_yagni_level(profile.yagni_level.level)
print(f"Claude YAGNI L{yagni.level}: reduction_cap={yagni.reduction_cap}%, quality_min={yagni.quality_minimum}%")

print("\nAll manual tests passed!")