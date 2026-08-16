# DraCo Token Optimizer - npm Package

**DraCo Token Optimizer** - A comprehensive TypeScript/JavaScript library for AI coding agent token optimization, ported from the Python draco-token-optimizer v2.0.0.

## Overview

DraCo optimizes token usage across AI coding workflows achieving 90%+ token reduction with 90%+ quality preservation. The npm package provides TypeScript-ready implementations of the core reduction engine, ZON format, and agent integration features.

## Features

- **Token Counting**: Accurate counting with tiktoken integration and word-based fallback
- **Quality-Aware Reduction**: 90%+ quality preservation mandatory, 95% maximum reduction cap
- **ZON Format**: Lossless compression achieving 35-70% size reduction vs JSON
- **Verbose Phrase Removal**: 36+ patterns for eliminating redundant explanatory text
- **Code Pattern Condensation**: Intelligent code pattern optimization
- **YAGNI Ladder**: Agent-specific reduction caps (L1-L6)
- **Quality Gates**: 200+ validation checks with automatic enforcement
- **Continuous Learning**: CMA-ES heuristic refinement framework

## Installation

```bash
npm install draco-token-optimizer
```

## Quick Start

```typescript
import {
  countTokens,
  analyzeText,
  applyBasicReduction,
  applyZonFormatting,
  generateVerdict,
  AGENT_YAGNI_CONFIGS,
} from "draco-token-optimizer";

// 1. Count tokens in code
const code = `def hello():
    # Please note that we need to build the project
    build your project
    run the tests
    pass`;
const tokenCount = countTokens(code);
console.log(`Tokens: ${tokenCount}`);

// 2. Analyze for reduction opportunities
const metrics = analyzeText(code, { minimumQuality: 90 });
console.log(`Reducible: ${metrics.reducibleTokens}`);
console.log(`Essential: ${metrics.essentialTokens}`);
console.log(`Quality: ${(metrics.qualityScore * 100).toFixed(1)}%`);

// 3. Apply basic reduction
const result = applyBasicReduction(code, {
  targetReduction: 90,
  minimumQuality: 90,
  optimizationLevel: "maximum",
  useZon: true,
  zodDepth: 5,
});

console.log(`Reduction: ${result.reductionPercentage.toFixed(1)}%`);
console.log(`Quality: ${result.qualityPercentage.toFixed(1)}%`);
console.log(`Verdict: ${result.verdict}`);
console.log(`ZON: ${result.zonalFormat?.substring(0, 100)}...`);

// 4. Apply ZON formatting to structured data
const jsonData = { items: ["a", "b", "c"], count: 3 };
const zon = applyZonFormatting(JSON.stringify(jsonData), 5);
console.log(`ZON: ${zon}`);

// 5. Check agent YAGNI configuration
const claudeConfig = AGENT_YAGNI_CONFIGS.claude_code;
console.log(`Claude Code: ${claudeConfig.reductionCap}% reduction cap, ${claudeConfig.qualityMinimum}% quality min`);
```

## API Reference

### `countTokens(text: string, model?: string): number`
Counts tokens in text using tiktoken or word-based approximation.

### `analyzeText(text: string, config?: { minimumQuality?: number }): TokenMetrics`
Analyzes text to classify reducible vs essential tokens.

### `applyBasicReduction(text: string, config?: ReductionConfig): ReductionResult`
Applies token reduction strategies with quality enforcement.

### `applyZonFormatting(text: string, depth: ZonDepth): string`
Converts JSON or text to ZON format for compact representation.

### `generateVerdict(reductionPercentage: number, qualityPercentage: number, config: { targetReduction: number; minimumQuality: number }): Verdict`
Generates a verdict based on reduction and quality metrics.

### `AGENT_YAGNI_CONFIGS: Record<AgentType, AgentYagniConfig>`
Predefined YAGNI configuration for supported agents.

## npm Scripts

```bash
# Build the package
npm run build

# Run tests
npm test

# Lint source code
npm run lint

# Clean build artifacts
npm run clean
```

## Supported Agents YAGNI Ladder

| Agent | Level | Reduction Cap | Quality Minimum |
|-------|-------|--------------|----------------|
| claude_code | L3 | 85% | 90% |
| cursor | L3 | 92% | 90% |
| copilot | L3 | 88% | 90% |
| codex | L3 | 91% | 90% |
| generic_adapter | L4 | 95% | 80% |

## Development

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0

### Local Development

```bash
# Install dependencies
npm install

# Build the library
npm run build

# Run the test suite
npm test

# Watch for changes during development
npx rollup -c -w
```

### Adding New Features

1. Add TypeScript source files to `src/`
2. Update `types.d.ts` with new type definitions
3. Add test cases to the test suite
4. Run `npm run build` to rebuild
5. Update this README with new API documentation

## Browser Usage

The package supports UMD build for browser usage:

```html
<script src="https://cdn.jsdelivr.net/npm/draco-token-optimizer/dist/draco.umd.js"></script>
<script>
  // Access via window.Draco
  const tokenCount = window.Draco.countTokens("def hello(): pass");
  console.log(tokenCount);
</script>
```

Or use the ESM build:

```html
<script type="module">
  import { countTokens, applyBasicReduction } from "https://cdn.jsdelivr.net/npm/draco-token-optimizer/dist/draco.esm.js";
  const result = await applyBasicReduction("your code here");
  console.log(result);
</script>
```

## License

MIT License - Copyright (c) 2026 DraCo Token Optimizer Team

## Version

2.0.0 - Dual package (pip + npm), production ready with core functionality