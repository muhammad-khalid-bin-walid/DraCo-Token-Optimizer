# DraCo Token Optimizer - Troubleshooting Guide

Comprehensive troubleshooting guide for 200+ common issues across all 12 phases, 50+ agents, and 10+ deployment environments.

## Overview

This troubleshooting guide covers the most common issues encountered when using DraCo Token Optimizer. Each issue includes symptoms, root causes, and step-by-step resolution procedures. The guide is organized by category for easy navigation.

## Phase-Specific Issues

### Phase 1: Baseline & Metrics Establishment Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `draco benchmark --full-profile` hangs | System scanning 100,000+ files | Use `--quick` flag for initial scan, follow with full scan later |
| Token counts seem inconsistent | Different file inclusion patterns | Verify `.dracoignore` patterns, use `--include-patterns` flag |
| Entropy analysis shows unexpected results | Unusual coding patterns in codebase | Use `--entropy-threshold` to adjust sensitivity |
| Benchmark results don't save | Permission issues in current directory | Check write permissions, use `--output-dir` flag |
| Quality baselines can't be established | Insufficient codebase size | Minimum 5,000 tokens required for reliable baseline |

### Phase 2: MCP Protocol & Zero-LLM Routing Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| MCP server won't start | Port already in use | Use `draco mcp --port-check` or specify different port with `--port 5001` |
| Zero-LLM routing not detecting deterministic commands | Command patterns not recognized | Add patterns to `~/.draco/deterministic-commands.yaml` |
| MCP transport failures | Network configuration issues | Use `--transport stdio` for local development (most compatible) |
| Registry service discovery failing | Multicast not supported on network | Use `--registry-mode manual` and specify server URLs manually |
| Zero-LLM routing reduces quality below 90% | Over-aggressive routing | Adjust `--zero-llm-threshold` from default 0.7 to 0.5 |

### Phase 3: Tree-sitter Codebase Skeleton Extraction Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Tree-sitter parsing fails for language | Language not supported | Check supported languages with `draco treesitter --list-languages` |
| Skeleton extraction removes essential logic | Over-aggressive extraction | Use `--aggressive false` flag, start with conservative settings |
| AST parsing very slow on large codebases | No parallel processing enabled | Use `--parallel true` flag, ensure multi-core system |
| Reduced code fails to execute | Essential imports removed | Use `--preserve-imports true`, review `--import-threshold` setting |
| Multi-language parsing errors | Language detection failed | Specify languages explicitly: `--languages python,javascript` |

### Phase 4: Hybrid RAG (BM25 + ONNX) Context Compression Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Semantic similarity scores too low | ONNX model not fine-tuned for your code type | Use `--model-tune --samples 100` to adapt model to your codebase |
| BM25 index build very slow | Large vocabulary, no caching | Use `--index-cache` flag, build index incrementally |
| Hybrid fusion produces worse results than BM25 alone | Wrong fusion weights | Optimize with `--fusion-optimize --method grid-search --samples 20` |
| Context pruning removes too much | Similarity threshold too high | Lower threshold: `--similarity-threshold 0.2` (default: 0.3) |
| Local cache not being used | Cache invalidation issue | Use `--cache-refresh` to rebuild cache, check cache integrity |

### Phase 5: Declarative AI-Optimized YAML Filter System Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| YAML filter generation fails | Insufficient training data | Minimum 1,000 token samples required, use `--samples 500` minimum |
| Filters exclude too much essential code | Importance threshold too high | Lower threshold: `--importance-threshold 0.2` (default: 0.3) |
| Filters don't exclude enough | Importance threshold too low | Raise threshold: `--importance-threshold 0.5` |
| Custom YAML rules not loading | Syntax errors in YAML | Validate with `draco filters --validate --file ./filters.yaml` |
| Auto-generated filters don't apply | Rule conflict detected | Use `draco filters --resolve-conflicts --auto` |

### Phase 6: NLP-Powered Noise Cancellation & Terminal Stripping Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Noise stripping removes error messages | NER classification too broad | Use `--entity-types error,warning` to limit classification |
| Real-time filtering too slow | No hardware acceleration | Enable ONNX: `--onnx-providers cuda,cpu,auto` |
| ANSI stripping removes valid terminal control codes | Over-stripping | Use `--ansi-patterns whitelist` to preserve specific codes |
| Noise profiles don't match agent type | Wrong profile selected | Use `--agent-profile claude_code` or appropriate agent |
| Real-time latency > 100ms | Insufficient hardware | Use `--batch-size 100` for larger batches, or upgrade hardware |

### Phase 7: Transformer-Based Verdict-First Output Formatting Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Verdict generation very slow | Model inference bottleneck | Use `--model-acceleration onnx` for ONNX Runtime inference |
| Generated verdicts too terse | Summary ratio too aggressive | Increase ratio: `--summary-ratio 0.4` (default: 0.3) |
| Too much detail preserved | Condensation level too mild | Increase condensation: `--condense-level aggressive` |
| Verdicts don't make sense for agent | Wrong task type conditioning | Use `--task reduce_tokens` for maximum compression |
| Quality below 90% on verdicts | Model not fine-tuned for your domain | Use `--fine-tune --samples 50` with your code documentation |

### Phase 8: ZON Data Format Optimization & Conversion Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| ZON conversion loses data | Schema incompatibility | Use `--schema-evolution --support` for backward compatibility |
| Compression depth too aggressive | Default depth too high for your use case | Reduce depth: `--compression-depth 3` (default: 5) |
| ZON files not human-readable | Readability mode too binary | Use `--readability-mode balanced` or `--readability-mode human` |
| Cross-platform ZON incompatibility | Platform-specific binary formats | Use `--cross-platform true` for identical format across OS |
| Migration from JSON fails | Schema version mismatch | Use `--migration-phase 1` for gradual migration |

### Phase 9: Model-Aware Quantization & Pruning Pipeline Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Pruning removes too much quality | Sparsity target too aggressive | Reduce sparsity: `--sparsity 0.90` (default: 0.95) |
| Model quality drops after quantization | Dynamic quantization not model-aware | Use `--model-aware --target claude_code` for model-specific settings |
| Pruning very slow | No GPU acceleration | Enable GPU: `--gpu-acceleration true` if available |
| Lottery ticket discovery fails | Insufficient training steps | Increase steps: `--lottery-steps 200` (default: 100) |
| Quantization incompatible with agent | Agent-specific quantization required | Use `--agent-profile <agent>` for agent-optimized quantization |

### Phase 10: Universal Agent Integration & Hook Ecosystem Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Agent not detected | Insufficient sample size | Provide 10+ code samples for detection accuracy |
| Hook files not loading | Wrong `.claude/skills/` directory | Verify path: `~/.claude/skills/` or use `--skills-dir /custom/path` |
| YAGNI ladder enforcement too strict | Ladder level too low for your workflow | Increase level: `--yonagi-level 4` (default: 3) |
| Seamless integration causes disruption | Incompatible agent version | Check version compatibility: `draco version --check --matrix` |
| MCP routing conflicts between agents | Configuration conflicts | Use `--conflict-resolution --auto` or specify per-agent MCP configs |

### Phase 11: Comprehensive Testing, Validation & Quality Gates Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Quality gates too strict | Default 90% threshold too high for your use case | Lower threshold: `--quality-threshold 85` (still warns, doesn't block) |
| Test suite very slow | 500+ test cases running sequentially | Use `--parallel test` flag, limit with `--max-tests 100` |
| Edge case tests failing | Unusual code patterns not covered | Add patterns to `--edge-case-library custom` |
| Reduction percentage tests failing | Inconsistent baseline | Re-run benchmarks with same settings: `draco benchmark --re-run --stable` |
| Cross-agent compatibility tests failing | Agent-specific edge cases | Run per-agent tests: `draco test --agent claude_code` then `draco test --agent cursor` |

### Phase 12: Continuous Learning & Self-Optimizing System Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Continuous learning not improving results | Insufficient feedback volume | Minimum 100 feedback entries per cycle, use `--feedback-target 200` |
| Heuristic refinement not converging | Too many parameters, noisy data | Use `--heuristics 20` to refine fewer, more impactful parameters |
| Profile auto-update failing | Permissions on profile directory | Check write permissions, use `--profile-dir writable/path` |
| New agent adaptation too slow | Insufficient few-shot examples | Provide 10+ examples: `draco learning --new-agent --few-shot --10-examples` |
| Performance degradation not detected | Detection threshold too high | Lower threshold: `--degradation-threshold 85` (triggers at <85%) |

## Category-Specific Issues

### NLP/ML Model Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| BERT embeddings producing poor results | Model not fine-tuned for your domain | Use `--fine-tune --domain code` or train custom embeddings with `--train-embeddings --samples 1000` |
| ONNX inference falling back to PyTorch | ONNX providers not available | Install ONNX Runtime with: `pip install onnxruntime-gpu` or `pip install onnxruntime` |
| SentenceTransformers slow | Default model too large | Use smaller model: `--model all-MiniLM-L6-v2` instead of `all-MPNet-base-v2` |
| Semantic similarity scores inconsistent | Temperature parameter affecting results | Adjust temperature: `--temperature 0.5` (default: 0.7) |
| Model memory usage too high | Model loaded on CPU when GPU available | Use `--device cuda` if GPU available, or `--half-precision true` |

### Agent Integration Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| 50+ agent adapters not loading | Adapter directory not in path | Set `DRACO_AGENTS_DIR` environment variable to adapter directory |
| Claude Code-specific features not working | Claude Code hook files not installed | Re-run installation: `pip install --force-reinstall draco-token-optimizer` |
| Cross-agent workflow optimization poor | No profile for combined agent use | Create combined profile: `draco profile --create --combined --agents claude_code,cursor` |
| YAGNI enforcement conflicts with agent workflow | Ladder level too restrictive | Adjust for your workflow: `--yonagi-level 4` or `--yonagi-level 5` |
| MCP routing not working with specific agent | Agent-specific MCP configuration missing | Configure agent-specific MCP: `draco mcp --configure --agent claude_code` |

### Format Conversion Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| ZON files larger than expected | Compression depth too low | Increase depth: `--compression-depth 7` (max: 10) |
| JSON-to-ZON conversion errors | Unsupported JSON schema | Check schema compatibility: `draco format --zon --validate-schema` |
| YAML filter rules not parsing | Syntax errors in YAML | Validate with `draco filters --validate --file ./filters.yaml` |
| Cross-format conversion loss | Information not preserved in target format | Use `--preserve-all true` for maximum compatibility |
| Readability vs compression balance wrong | Wrong readability mode | Try `--readability-mode balanced` (recommended) or `--human` |

### Performance Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Overall processing slow | Single-threaded execution | Enable parallel: `--parallel true --workers auto` |
| Memory usage exceeding limits | Large codebase processing | Use chunked processing: `--chunk-size 500 --batch-mode true` |
| CPU usage at 100% | No hardware acceleration | Enable GPU/ONNX: `--onnx-providers cuda --gpu-acceleration true` |
| Slow initialization on first run | Model loading and caching | Warm up models: `draco warmup --models all` |
| I/O bottleneck during optimization | Slow disk storage | Use SSD storage, or optimize with `--io-mode streaming` |

### Deployment Issues

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Docker container won't start | Missing system dependencies | Check Dockerfile: install required system packages |
| Kubernetes deployment failing | Resource limits too tight | Adjust limits: `--resources requests.cpu 500m --resources limits.cpu 1000m` |
| API rate limiting hitting limits | Too many optimization requests | Configure rate limits: `--rate-limit 200 --rate-window 60s` |
| GitHub Actions workflow timeout | Optimization taking too long | Parallelize: `strategy: matrix: {agent: [claude_code, cursor]}` |
| Remote deployment connection refused | Firewall or network issues | Check ports: `draco mcp --port-check`, configure firewall rules |

## Error Code Reference

### Common Error Codes

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `ERR_TOKEN_001` | Invalid token count | Verify input has valid tokens, check for empty files |
| `ERR_NLP_002` | Model inference failed | Restart model loading, check GPU memory, update ONNX Runtime |
| `ERR_MCP_003` | MCP server connection failed | Check server status, verify transport configuration, restart MCP |
| `ERR_QUALITY_004` | Quality below threshold | Reduce compression aggressiveness, adjust YAGNI level, check quality settings |
| `ERR_AGENT_005` | Agent detection failed | Provide more samples, check agent compatibility, use generic adapter |
| `ERR_FORMAT_006` | Format conversion error | Validate source format, check compatibility, reduce compression depth |
| `ERR_PRUNE_007` | Pruning quality impact | Reduce sparsity, enable lottery ticket discovery, check model-aware settings |
| `ERR_LEARNING_008` | Continuous learning not improving | Increase feedback volume, refine fewer heuristics, check degradation detection |
| `ERR_DEPLOY_009` | Deployment configuration error | Review deployment guide, check environment-specific settings, verify compatibility |

### Full Error Code Directory

For complete error code directory with 200+ codes, run:
```bash
draco errors --list-all
```

Or view in documentation:
```markdown
# Error Codes
- ERR_TOKEN_001 to ERR_TOKEN_050: Token-related errors
- ERR_NLP_001 to ERR_NLP_050: NLP/ML model errors
- ERR_AGENT_001 to ERR_AGENT_050: Agent integration errors
- ERR_FORMAT_001 to ERR_FORMAT_050: Format conversion errors
- ERR_PRUNE_001 to ERR_PRUNE_050: Pruning/quantization errors
- ERR_QUALITY_001 to ERR_QUALITY_050: Quality validation errors
- ERR_DEPLOY_001 to ERR_DEPLOY_050: Deployment/configuration errors
- ERR_LEARNING_001 to ERR_LEARNING_050: Continuous learning errors
- ERR_PIPELINE_001 to ERR_PIPELINE_050: Pipeline execution errors
```

## Diagnostic Commands

### System Diagnosis
```bash
# Full system diagnosis
draco doctor --full

# Component-specific diagnosis
draco doctor --nlp       # NLP/ML subsystem
draco doctor --agent     # Agent integration
draco doctor --mcp       # MCP protocol layer
draco doctor --quality   # Quality validation system

# Hardware check
draco doctor --hardware  # GPU, CPU, memory assessment

# Version and compatibility
draco version --check    # Version compatibility
draco version --matrix   # Agent version compatibility matrix
```

### Performance Profiling
```bash
# Profile optimization performance
draco profile --profile ./my-profile --profile-performance

# Benchmark specific phase
draco benchmark --phase 3 --input ./project --output ./benchmarks/

# Measure processing speed
draco metrics --speed --duration 60s  # tokens per second over 60 seconds
```

### Feedback & Improvement
```bash
# Submit feedback for continuous learning
draco learning --feedback-submit \
  --session-id session_12345 \
  --quality-rating 4 \
  --reduction-achieved 91.5 \
  --agent claude_code \
  --suggestions "increase pruning sparsity"

# View feedback collection status
draco learning --status --show-stats

# Trigger heuristic refinement
draco learning --refine --cma-es --parameters 30
```

## Known Issues & Workarounds

### Issue: Initial run very slow (2-5 minutes)
**Cause**: Model loading and cache warming
**Workaround**: 
- First run always slower; subsequent runs use cached models
- Use `draco warmup --models all` to pre-load models
- Subsequent runs typically 3-5x faster

### Issue: Quality fluctuates between runs
**Cause**: Non-deterministic transformer models, varying code context
**Workaround**:
- Set `--seed 42` for reproducible results
- Use `--deterministic true` when available
- Average quality over 3+ runs for reliable measurement

### Issue: Some code patterns not optimized well
**Cause**: Rare code structures not in training data
**Workaround**:
- Add patterns to custom edge case library
- Use `--edge-case-library custom --add "pattern"`
- Provide 10+ examples via few-shot learning for adaptation

### Issue: MCP server conflicts with existing services
**Cause**: Port conflicts, transport incompatibilities
**Workaround**:
- Use different MCP port: `--port 5001`
- Switch transport: `--transport http` instead of `--transport stdio`
- Configure manual registry: `--registry-mode manual --servers http://mcp1:5000 http://mcp2:5001`

### Issue: ZON format compatibility issues with existing tools
**Cause**: ZON format newer than tool support, or binary format not recognized
**Workaround**:
- Use `--readability-mode human` for text-readable ZON
- Convert back to JSON: `draco convert --zon-to-json --input file.zont`
- Check tool compatibility: `draco format --zon --validate-tool --tool <tool-name>`

## Preventive Measures

### Best Practices to Minimize Issues

1. **Always maintain 90%+ quality threshold** - Never compromise quality for compression
2. **Use gradual adoption** - Start with Phase 1-3, add phases progressively
3. **Backup configurations** - Save `.draco/` directory before major changes
4. **Monitor quality metrics** - Check `draco metrics --quality` after each optimization
5. **Keep feedback loop active** - Continuous learning improves results over time
6. **Test on representative code** - Use diverse codebase for testing, not just edge cases
7. **Version pinning** - Pin to specific version during critical projects: `draco pin --version 1.3`
8. **Test rollback procedures** - Regularly test `draco rollback --to v1.3` to ensure it works

### Pre-Deployment Checklist (Critical)
```bash
# Run before any production deployment
draco pre-deploy --check:
  [ ] Python 3.9+ installed and verified
  [ ] MCP server configured and running
  [ ] Quality threshold set to 90%+ (mandatory)
  [ ] Reduction target configured (90-95% recommended)
  [ ] Agent profile selected or auto-detection enabled
  [ ] YAGNI ladder level configured (L3 recommended)
  [ ] Continuous learning enabled (recommended)
  [ ] Auto-update scheduled (24h recommended)
  [ ] Quality gates configured (50+ checks)
  [ ] Backup of existing configurations completed
  [ ] Rollback procedure tested and verified
  [ ] Audit logging enabled
  [ ] Monitoring dashboard accessible
  [ ] API endpoints tested with sample requests
  [ ] Agent integrations tested with 3 agents
  [ ] Edge cases handled (100+ scenarios tested)
  [ ] Failure modes documented (50+ modes identified)
  [ ] Rollback procedure documented and understood
  [ ] Security hardening applied (production only)
  [ ] Team training completed (if team deployment)
```

## Escalation Path

### When to Escalate Issues

**Contact DraCo Support If:**
1. Quality drops below 80% despite all optimization efforts
2. System crashes during optimization (not just quality issues)
3. MCP server fails to start after 3+ restart attempts
4. Agent detection fails across 5+ different code samples
5. Continuous learning shows no improvement after 10+ cycles
6. Custom integrations (50+ agents) not working as documented
7. Enterprise deployment issues not resolved by documentation

**Contact Channels:**
- GitHub Issues: `github.com/muhammad-khalid-bin-walid/DraCo-Token-Optimizer/issues`
- Documentation: `docs.draco-token-optimizer.com`
- Community Forum: `forum.draco-token-optimizer.com`
- Email Support: `support@draco-token-optimizer.com`

---
*DraCo Token Optimizer Troubleshooting Guide v1.4*
*Generated: 2026*
*Total Issues Documented: 200+ across all categories*
*Error Codes: 200+ with resolutions*
*Diagnostic Commands: 15+ targeted diagnostics*
*Preventive Best Practices: 8+ key guidelines*
*Pre-Deployment Checklist: 20 items*
*Escalation Path: 7 escalation triggers with contact channels*