import sys
import os

# Add draco package to path
sys.path.insert(0, 'draco-token-optimizer')
sys.path.insert(0, os.path.dirname('draco-token-optimizer'))

# Check config
from draco.config import get_reduction_target, get_quality_threshold
red = get_reduction_target()
qlt = get_quality_threshold()
print(f'Config: reduction={red}%, quality={qlt}%')

# Check dashboard
from draco.dashboard import quick_health_check
result = quick_health_check()
print(f'Dashboard: reduction={result["reduction"]}%, quality={result["quality"]}%, mandates={result["mandates_pass"]}, healthy={result["healthy"]}')

# Check skills
from pathlib import Path
skills_dir = Path('draco-token-optimizer/.claude/skills')
skills = [f.name for f in skills_dir.glob('*.skill')]
print(f'Skills ({len(skills)}): {skills}')

# Check workflows
import yaml
workflows_dir = Path('draco-token-optimizer/.github/workflows')
workflows = [f.name for f in workflows_dir.glob('*.yml')]
print(f'Workflows ({len(workflows)}): {workflows}')

# Check onboarding guide
onboard = Path('draco-token-optimizer/docs/ONBOARDING_GUIDE.md')
print(f'Onboarding guide: {onboard.exists()}')

# Check status
status = Path('draco-token-optimizer/status.md')
print(f'Status: {status.exists()}')

# Verify all workflows are valid YAML
print('\\n--- Workflow Validation ---')
for wf in workflows:
    import yaml
    try:
        yaml.safe_load(open(f'draco-token-optimizer/.github/workflows/{wf}'))
        print(f'  {wf}: VALID')
    except Exception as e:
        print(f'  {wf}: INVALID - {e}')

print('\\n--- Final Review Complete ---')