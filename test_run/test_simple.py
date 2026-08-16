"""Simple DraCo Token Optimizer test"""
import sys
sys.path.insert(0, 'draco-token-optimizer')

# Test 1: Core imports
try:
    from draco.core.reducer import count_tokens, analyze_text, apply_basic_reduction
    print("✓ Test 1 PASSED: Core reducer imports")
except Exception as e:
    print(f"✗ Test 1 FAILED: {e}")

# Test 2: Config imports and validation
try:
    from draco.config import validate_config, get_reduction_target, get_quality_threshold
    issues = validate_config()
    print(f"✓ Test 2 PASSED: Config imports, {len(issues)} validation issues")
except Exception as e:
    print(f"✗ Test 2 FAILED: {e}")

# Test 3: Dashboard imports
try:
    from draco.dashboard import quick_health_check
    health = quick_health_check()
    print(f"✓ Test 3 PASSED: Dashboard import, healthy={health['healthy']}")
except Exception as e:
    print(f"✗ Test 3 FAILED: {e}")

# Test 4: CLI imports
try:
    from draco.cli import main
    print("✓ Test 4 PASSED: CLI imports")
except Exception as e:
    print(f"✗ Test 4 FAILED: {e}")

# Test 5: Basic functionality
try:
    from draco.core.reducer import count_tokens, analyze_text
    text = "def hello():\n    # Please note that this works"
    tokens = count_tokens(text)
    metrics = analyze_text(text)
    print(f"✓ Test 5 PASSED: count_tokens={tokens}, quality={metrics.quality_score:.2f}")
except Exception as e:
    print(f"✗ Test 5 FAILED: {e}")

# Test 6: Config thresholds
try:
    from draco.config import MINIMUM_QUALITY_PRESERVATION, MAXIMUM_TOKEN_REDUCTION
    print(f"✓ Test 6 PASSED: Min quality={MINIMUM_QUALITY_PRESERVATION}%, Max reduction={MAXIMUM_TOKEN_REDUCTION}%")
except Exception as e:
    print(f"✗ Test 6 FAILED: {e}")

print("\n=== TEST SUITE COMPLETE ===")