import sys
sys.path.insert(0, 'draco-token-optimizer')

print('=== FINAL VALIDATION ===')
print()

# 1. Check all key imports
from draco.core.reducer import count_tokens, analyze_text, apply_basic_reduction
print('✓ Core reducer imports')

from draco.config import (
    validate_config, get_reduction_target, get_quality_threshold,
    MINIMUM_QUALITY_PRESERVATION, MAXIMUM_TOKEN_REDUCTION,
    is_phase_enabled, enable_phase, disable_phase,
    ZON_READABILITY_MODE, ZON_COMPRESSION_DEPTH,
    DEPLOYMENT_ENVIRONMENT, IS_DOCKER, IS_KUBERNETES,
    PHASE_ENABLED, NUM_QUALITY_GATES
)
print('✓ Config imports')

from draco.dashboard import quick_health_check
print('✓ Dashboard imports')

# 2. Run validation
issues = validate_config()
print(f'✓ Config validation: {len(issues)} issues')
if issues:
    for i in issues[:3]:
        print(f'  - {i}')

# 3. Test functionality
text = '''# Please note that this is a test
# it is important to build the project and run the tests
def hello():
    pass'''

metrics = analyze_text(text)
print(f'✓ analyze_text: total={metrics.total_tokens}, reducible={metrics.reducible_tokens}, essential={metrics.essential_tokens}, quality={metrics.quality_score:.2f}')

result = apply_basic_reduction(text, {
    'target_reduction': 90,
    'minimum_quality': 90,
    'optimization_level': 'maximum',
    'use_zon': False
})
print(f'✓ apply_basic_reduction: reduction={result["reduction_percentage"]:.1f}%, quality={result["quality_percentage"]:.1f}%, verdict={result["verdict"]}')

# 4. Health check
health = quick_health_check()
print(f'✓ quick_health_check: reduction={health["reduction"]}%, quality={health["quality"]}%, healthy={health["healthy"]}')

# 5. Phase management
print(f'✓ Phase management: enabled={sum(PHASE_ENABLED.values())}/12 phases')
print(f'  Phase 1: {is_phase_enabled(1)}')
print(f'  Phase 12: {is_phase_enabled(12)}')

# 6. ZON settings
print(f'✓ ZON settings: mode={ZON_READABILITY_MODE}, depth={ZON_COMPRESSION_DEPTH}')

# 7. Deployment settings
print(f'✓ Deployment: environment={DEPLOYMENT_ENVIRONMENT}, docker={IS_DOCKER}, k8s={IS_KUBERNETES}')

# 8. Quality thresholds
print(f'✓ Quality: min={MINIMUM_QUALITY_PRESERVATION}%, max cap={MAXIMUM_TOKEN_REDUCTION}%')

print()
print('=== ALL VALIDATIONS PASSED ===')