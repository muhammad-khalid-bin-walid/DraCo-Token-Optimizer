import sys
sys.path.insert(0, 'draco-token-optimizer')
from draco.dashboard import quick_health_check, show_detailed_dashboard, export_dashboard, check_agent_compatibility, QualityTracker, PhaseTracker, AgentTracker

# Test quick health check
result = quick_health_check()
print('=== Quick Health Check ===')
for key, value in result.items():
    print(f'  {key}: {value}')

print()

# Test export
md = export_dashboard('markdown')
print('=== Markdown Export ===')
print(md)

print()

# Test agent compatibility
compat = check_agent_compatibility('claude_code')
print('=== Agent Compatibility: claude_code ===')
for key, value in compat.items():
    print(f'  {key}: {value}')

print()

# Test QualityTracker
print('=== QualityTracker ===')
tracker = QualityTracker()
tracker.record(85, 92)
trends = tracker.get_trends()
for key, value in trends.items():
    print(f'  {key}: {value}')

print()

# Test PhaseTracker
print('=== PhaseTracker ===')
tracker = PhaseTracker()
print(f'  Phases complete: {tracker.phases_complete}/12')
for i in range(1, 4):
    print(f'  Phase {i}: {tracker.get_phase_status(i)}')

print()

# Test AgentTracker
print('=== AgentTracker ===')
tracker = AgentTracker()
all_agents = tracker.get_all_agents()
for name, profile in all_agents.items():
    print(f'  {name}: reduction_cap={profile["reduction_cap"]}%, quality_min={profile["quality_minimum"]}%')

print()

# Show detailed dashboard
print('=== Dashboard Output ===')
show_detailed_dashboard()

print()
print('=== All Tests Passed ===')