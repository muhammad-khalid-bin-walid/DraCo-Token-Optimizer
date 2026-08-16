# DraCo Token Optimizer - Community Onboarding Guide

Welcome to DraCo! This guide helps new developers and users get started with the token optimization system.

## Quick Start

### Prerequisites
- Python 3.13+
- Git
- Access to the DraCo repository

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/draco-token-optimizer.git
cd draco-token-optimizer

# Install the package
pip install -e draco-token-optimizer/draco/

# Install development dependencies
pip install -r draco-token-optimizer/requirements-dev.txt

# Verify installation
python -c "import draco; print('DraCo v1.0 ready')"
```

### First-Run Verification

```bash
python -c "
import sys
sys.path.insert(0, 'draco-token-optimizer')

from draco.config import get_reduction_target, get_quality_threshold
from draco.core.reducer import analyze_text, apply_basic_reduction

# Verify 90%+ mandates
reduction = get_reduction_target()
quality = get_quality_threshold()
assert reduction >= 90, f'Reduction target must be 90%+, got {reduction}%'
assert quality >= 90, f'Quality threshold must be 90%+, got {quality}%'
print(f'✓ Reduction target: {reduction}%')
print(f'✓ Quality threshold: {quality}%')

# Test basic reduction
metrics = analyze_text('This is a test sentence with some repetitive phrases that can be reduced while preserving essential technical information.')
result = apply_basic_reduction('This is a test sentence with some repetitive phrases that can be reduced.')
print(f'✓ Analysis: reducible={metrics.reducible_tokens}, essential={metrics.essential_tokens}')
print(f'✓ Reduction: {result[\"reduction_percentage\"]:.1f}%, Quality: {result[\"quality_percentage\"]:.1f}%')
print('✓ DraCo token optimizer is operational!')
"
```

## Project Structure

```
draco-token-optimizer/
├── .claude/skills/        # 12 phase-specific skill files
├── draco/                  # Python package (9 modules)
│   ├── config.py           # 500+ configuration settings
│   ├── core/reducer.py     # Token reduction engine
│   ├── nlp/embeddings.py   # Sentence embeddings (384-dim fallback)
│   ├── nlp/classification.py  # Intent detection
│   ├── agents.py           # YAGNI ladder + 50+ agent profiles
│   ├── quantization.py     # Pruning & quantization pipelines
│   └── mcp.py              # Model Context Protocol / zero-LLM routing
├── .github/workflows/      # 5 CI/CD workflows
├── docs/                   # 28+ documentation files
├── tests/                  # Test suites
└── README.md               # Project overview
```

## 12 Phases Overview

| Phase | Focus | Key Deliverable |
|-------|-------|-----------------|
| 1 | Baseline & Metrics | Token counting, quality assessment |
| 2 | MCP Protocol | Zero-LLM routing, deterministic commands |
| 3 | Tree-sitter | Codebase skeleton parsing |
| 4 | Hybrid RAG | BM25 + ONNX semantic retrieval |
| 5 | YAML Filters | Importance/frequency-based filtering |
| 6 | NLP Noise Cancellation | Verbose phrase removal |
| 7 | Verdict-First | Transformer-based output formatting |
| 8 | ZON Format | Lossless compression (35-70% vs JSON) |
| 9 | Quantization/Pruning | Model-aware sparsity targets |
| 10 | Agent Integration | 50+ agents, YAGNI ladder L1-L6 |
| 11 | Testing & Validation | 200+ quality gates |
| 12 | Continuous Learning | Feedback loops, auto-optimization |

## Supported AI Agents (50+)

DraCo integrates with these AI agents via the YAGNI-first decision ladder:

- **claude_code** - YAGNI L3 (balanced), 85% reduction cap, 90% quality minimum
- **cursor** - YAGNI L3, 92% sparsity target
- **copilot** - YAGNI L3, 88% sparsity target  
- **codex** - YAGNI L3, 91% sparsity target
- **generic_adapter** - YAGNI L4 (maximum), configurable

### YAGNI Decision Ladder

| Level | Reduction Cap | Quality Minimum | Use Case |
|-------|--------------|-----------------|----------|
| L1 | 70% | 95% | Conservative, safety-critical |
| L2 | 80% | 92% | Standard development |
| L3 | 85% | 90% | **Default (recommended)** |
| L4 | 90% | 85% | Aggressive optimization |
| L5 | 95% | 80% | Maximum reduction |
| L6 | 98% | 50% | Experimental, research |

## Configuration

All settings are in `draco/config.py` with 500+ configurable parameters. Key settings:

- `REDUCTION_TARGET`: Default 90% (minimum acceptable)
- `QUALITY_THRESHOLD`: Default 90% (mandatory preservation)
- `YAGNI_LEVEL`: Default L3 (balanced)
- `ZON_COMPRESSION_DEPTH`: 1-10 (default 5)
- `MCP_CONFIDENCE_THRESHOLD`: 0.7 (zero-LLM routing)

## Running Tests

```bash
# Run all tests
python -m pytest draco-token-optimizer/draco/tests/

# Run specific test categories
python -m pytest draco-token-optimizer/draco/tests/ -k "quality"
python -m pytest draco-token-optimizer/draco/tests/ -k "agent"
python -m pytest draco-token-optimizer/draco/tests/ -k "quantization"
```

## CI/CD Workflows

The project uses GitHub Actions with 5 workflows:

- `ci-cd.yml` - Continuous integration and deployment
- `reduction-optimization.yml` - Reduction algorithm tests
- `quantization-agent.yml` - Quantization & agent compatibility
- `mcp-protocol.yml` - MCP protocol validation
- `quality-gates.yml` - Quality gate verification

## Getting Help

- **Documentation**: See `docs/` directory for 28+ files
- **Skills**: `.claude/skills/` has 12 phase-specific skill files
- **Issues**: Check `troubleshooting.md` for 200+ common issues
- **API**: See `api_reference.md` for 200+ endpoints

## Contributing

1. Follow the 12-phase plan in `plan.md`
2. Maintain 90%+ token reduction with 90%+ quality preservation
3. Use YAGNI-first decision ladder for agent integration
4. All changes documented in `status.md`
5. Run quality gates before committing

## License

This project is licensed under the MIT License - see the repository for details.

---

**Need help?** Open an issue or check the troubleshooting documentation for common problems.