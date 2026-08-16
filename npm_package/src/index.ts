/* DraCo Token Optimizer - TypeScript Port
 * Comprehensive token reduction for AI coding agents
 * Based on the Python draco-token-optimizer v2.0.0
 */

import {
  countTokens as countTokensPy,
  analyzeText as analyzeTextPy,
  applyBasicReduction as applyBasicReductionPy,
  TokenMetrics,
  ReductionResult,
} from "./reducer";

// ============================================================
// Token Counting
// ============================================================

/**
 * Count the number of tokens in a text string.
 * Uses tiktoken under the hood when available, falls back to approximation.
 * @param text The text to count tokens in
 * @param model Target model for tiktoken encoding (default: gpt-4)
 * @returns Number of tokens
 */
export function countTokens(text: string, model: string = "gpt-4"): number {
  if (!text) return 0;

  // Try to use tiktoken if available (will be bundled or runtime)
  try {
    // Dynamic import - tiktoken may or may not be available
    // If not available, fall through to approximation
    const { encodingForModel } = require("tiktoken");
    const encoding = encodingForModel(model);
    return encoding.encode(text).length;
  } catch {
    // Fallback: word-based approximation
    // Code: ~1.3 tokens/word, Prose: ~1.5 tokens/word
    const codePatterns = [
      "def ",
      "import ",
      "class ",
      "function ",
      "const ",
      "let ",
      "var ",
      "for ",
      "while ",
      "if ",
      "else ",
      "return ",
      "=>",
      "/*",
      "*/",
      ".py",
      ".js",
      ".ts",
    ];

    const lowerText = text.toLowerCase();
    const isCode = codePatterns.some((p) => lowerText.includes(p));
    const tokenPerWord = isCode ? 1.3 : 1.5;
    const words = text.split();
    const tokenCount = Math.floor(words.length * tokenPerWord);
    return Math.max(1, tokenCount);
  }
}

/**
 * Count tokens with explicit tiktoken availability check
 * @param text The text to count
 * @returns Token count or -1 if tiktoken not available
 */
export function countTokensExplicit(text: string): [number, boolean] {
  if (!text) return [0, false];

  try {
    const { encodingForModel } = require("tiktoken");
    const encoding = encodingForModel("cl100k_base");
    const tokens = encoding.encode(text);
    return [tokens.length, true];
  } catch {
    return [countTokens(text), false];
  }
}

// ============================================================
// Text Analysis
// ============================================================

/**
 * Analyze text to determine reduction opportunities.
 * Returns TokenMetrics with reducible vs essential classification.
 * @param text The text to analyze
 * @param config Optional compression configuration
 * @returns TokenMetrics with analysis results
 */
export function analyzeText(
  text: string,
  config?: {
    minimumQuality?: number;
    targetReduction?: number;
  }
): TokenMetrics {
  // Use the Python port analysis as base, adapted for TS
  let totalTokens = countTokens(text);

  if (totalTokens === 0) {
    return {
      totalTokens: 0,
      reducibleTokens: 0,
      essentialTokens: 0,
      compressionRatio: 0.0,
      qualityScore: 1.0,
      reductionAchieved: 0.0,
      belowThreshold: false,
    };
  }

  // Enhanced verbose phrase patterns (port from Python)
  const verbosePatterns = [
    "is important to note that",
    "please note that",
    "it should be noted that",
    "it is worth noting that",
    "one should consider",
    "it is crucial that",
    "it is worth mentioning that",
    "it should be mentioned that",
    "as a matter of fact",
    "in case you were not aware",
    "it is interesting to note",
    "it is important to mention",
    "please be advised that",
    "it is essential to understand",
    "it is necessary to note",
    "one must consider",
    "it is significant to note",
    "it is useful to note",
    "it is helpful to note",
    "it is appropriate to note",
    "it is advisable to note",
    "it is pertinent to note",
    "it is relevant to note",
    "it is valuable to note",
    "it is critical to note",
    "it is indispensable to note",
    "it is vital to note",
    "it is essential to mention",
    "it is necessary to mention",
    "it is important to mention",
    "it is worth mentioning",
    "one should note",
    "one must note",
  ];

  let reducible = 0;
  let essential = 0;

  const lowerText = text.toLowerCase();
  const lines = text.split("\n");

  for (const line of lines) {
    const stripped = line.trim();

    if (!stripped) continue;

    // Count comments (reducible in most cases)
    if (stripped.startsWith("#") || (stripped.startsWith("//") && !stripped.includes("{"))) {
      reducible += countTokens(line);
      continue;
    }

    // Count verbose explanatory phrases
    let verboseDetected = false;
    for (const pattern of verbosePatterns) {
      if (lowerText.includes(pattern)) {
        // Mark as reducible but keep essence
        reducible += Math.floor(countTokens(line) * 0.6);
        essential += Math.floor(countTokens(line) * 0.4);
        verboseDetected = true;
        break;
      }
    }

    if (verboseDetected) continue;

    // Count repetitive structures
    if (stripped.startsWith("build ") || stripped.startsWith("run ")) {
      reducible += Math.floor(countTokens(line) * 0.3);
      essential += Math.floor(countTokens(line) * 0.7);
      continue;
    }

    // Default: assume essential
    essential += countTokens(line);
  }

  // Default heuristics if nothing analyzed
  if (reducible + essential === 0) {
    reducible = Math.floor(totalTokens * 0.4);
    essential = totalTokens - reducible;
  }

  const compressionRatio = reducible / totalTokens;
  const qualityScore = essential / totalTokens;
  const reductionAchievable = compressionRatio * 100;

  const minimumQuality = config?.minimumQuality ?? 90;
  const belowThreshold = qualityScore * 100 < minimumQuality;

  return {
    totalTokens,
    reducibleTokens: reducible,
    essentialTokens: essential,
    compressionRatio: Number(compressionRatio.toFixed(4)),
    qualityScore: Number(qualityScore.toFixed(4)),
    reductionAchieved: Number(reductionAchievable.toFixed(2)),
    belowThreshold,
  };
}

// ============================================================
// Reduction Strategies
// ============================================================

/**
 * Apply basic token reduction strategies to text.
 * @param text The text to reduce
 * @param config Compression configuration
 * @returns ReductionResult with metrics and verdict
 */
export function applyBasicReduction(
  text: string,
  config?: {
    targetReduction?: number;
    minimumQuality?: number;
    optimizationLevel?: "conservative" | "balanced" | "maximum";
    useZon?: boolean;
    zodDepth?: number;
  }
): ReductionResult {
  // Default config
  const defaults = {
    targetReduction: config?.targetReduction ?? 90,
    minimumQuality: config?.minimumQuality ?? 90,
    optimizationLevel: config?.optimizationLevel ?? "maximum",
    useZon: config?.useZon ?? false,
    zodDepth: config?.zodDepth ?? 5,
  };

  if (!text || !text.trim()) {
    return {
      originalTokens: 0,
      reducedTokens: 0,
      remainingTokens: 0,
      reductionPercentage: 0.0,
      qualityPercentage: 100.0,
      passedQualityGate: true,
      verdict: "no_content",
      zonalFormat: null,
      metadata: {
        metrics: {
          totalTokens: 0,
          reducibleTokens: 0,
          essentialTokens: 0,
          compressionRatio: 0.0,
        },
        config: {
          targetReduction: defaults.targetReduction,
          minimumQuality: defaults.minimumQuality,
          optimizationLevel: defaults.optimizationLevel,
          useZon: defaults.useZon,
          agentType: "auto_detect",
        },
      },
    };
  }

  // Analyze the text
  const metrics = analyzeText(text, {
    minimumQuality: defaults.minimumQuality,
  });

  // Apply reduction strategies
  let reduced = text;

  // Strategy 1: Remove verbose explanatory phrases
  const verbosePatterns: Array<[string, string]> = [
    ["is important to note that", ""],
    ["please note that", ""],
    ["it should be noted that", ""],
    ["it is worth noting that", ""],
    ["one should consider", ""],
    ["it is crucial that", ""],
  ];

  const lowerReduced = reduced.toLowerCase();
  for (const [pattern, replacement] of verbosePatterns) {
    const regex = new RegExp(pattern, "i");
    if (regex.test(lowerReduced)) {
      reduced = reduced.replace(regex, replacement);
    }
  }

  // Strategy 2: Compress repetitive build/run commands
  reduced = reduced.replace(/build\s+your\s+project/gi, "build_project");
  reduced = reduced.replace(/run\s+the\s+tests/gi, "run_tests");
  reduced = reduced.replace(/run\s+your\s+code/gi, "run_code");

  // Strategy 3: Remove filler words and phrases
  const fillerPatterns: Array<[string, string]> = [
    [/\bvery\s+/g, ""],
    [/\breally\s+/g, ""],
    [/\babsolutely\s+/g, ""],
  ];

  for (const [pattern, replacement] of fillerPatterns) {
    reduced = reduced.replace(pattern, replacement);
  }

  // Strategy 4: Condense common code patterns
  const codePatterns: Array<[RegExp, string]> = [
    [/for\s+\w+\s+in\s+/g, "for _ in "],
    [/if\s+\w+\s+is\s+/g, "if "],
    [/while\s+\w+\s+is\s+/g, "while "],
  ];

  for (const [pattern, replacement] of codePatterns) {
    reduced = reduced.replace(pattern, replacement);
  }

  // Strategy 5: Remove transitional phrases
  reduced = reduced.replace(/\bto note that\b/gi, "");
  reduced = reduced.replace(/\bAs a result\b/gi, "");
  reduced = reduced.replace(/\bAs a consequence\b/gi, "");
  reduced = reduced.replace(/\bConsequently\b/gi, "");
  reduced = reduced.replace(/\bTherefore\b/gi, "");
  reduced = reduced.replace(/\bHence\b/gi, "");

  // Count tokens in reduced version
  const reducedTokens = countTokens(reduced);
  const originalTokens = countTokens(text);

  // Calculate metrics
  const reductionPercentage =
    originalTokens > 0
      ? ((originalTokens - reducedTokens) / originalTokens) * 100
      : 0.0;
  const qualityPercentage =
    originalTokens > 0 ? (reducedTokens / originalTokens) * 100 : 100.0;

  // Check quality gate
  const passedQualityGate = qualityPercentage >= defaults.minimumQuality;

  // Generate verdict
  let verdict: string;
  if (reductionPercentage >= defaults.targetReduction && qualityPercentage >= defaults.minimumQuality) {
    verdict = "reduce_tokens";
  } else if (reductionPercentage >= defaults.targetReduction * 0.7 && qualityPercentage >= defaults.minimumQuality) {
    verdict = "preserve_quality";
  } else if (reductionPercentage < defaults.targetReduction * 0.3 && qualityPercentage >= defaults.minimumQuality) {
    verdict = "minimal_change";
  } else if (reductionPercentage >= defaults.targetReduction && qualityPercentage < defaults.minimumQuality) {
    verdict = "quality_compromise";
  } else if (reductionPercentage < defaults.targetReduction * 0.3 && qualityPercentage < defaults.minimumQuality) {
    verdict = "restore_original";
  } else {
    verdict = "optimize_readability";
  }

  // Apply ZON formatting if enabled
  let zonalFormat: string | null = null;
  if (defaults.useZon) {
    zonalFormat = applyZonFormatting(reduced, defaults.zodDepth);
  }

  // Build metadata
  const metadata = {
    metrics: {
      totalTokens: metrics.totalTokens,
      reducibleTokens: metrics.reducibleTokens,
      essentialTokens: metrics.essentialTokens,
      compressionRatio: metrics.compressionRatio,
    },
    config: {
      targetReduction: defaults.targetReduction,
      minimumQuality: defaults.minimumQuality,
      optimizationLevel: defaults.optimizationLevel,
      useZon: defaults.useZon,
      agentType: "auto_detect",
    },
  };

  return {
    originalTokens,
    reducedTokens,
    remainingTokens: reducedTokens,
    reductionPercentage: Number(reductionPercentage.toFixed(2)),
    qualityPercentage: Number(qualityPercentage.toFixed(2)),
    passedQualityGate,
    verdict,
    zonalFormat,
    metadata,
  };
}

// ============================================================
// ZON Formatting
// ============================================================

/**
 * Apply ZON (Zoned Object Notation) formatting for compact representation.
 * ZON is a lossless compression format that can achieve 35-70% size reduction vs JSON.
 * @param text The text to format
 * @param depth Compression depth (1-10, default: 5)
 * @returns ZON-formatted string
 */
export function applyZonFormatting(text: string, depth: number = 5): string {
  // ZON compression depth validation
  const d = Math.max(1, Math.min(10, depth));

  if (!text) return "";

  // Check if text is JSON-like and can be parsed
  try {
    const JSON = require("json"); // Will fail, using native
  } catch {
    // Native JSON available
  }

  const nativeJSON: any = window?.JSON || require("json");

  try {
    const data = nativeJSON.parse(text);

    if (typeof data === "object" && !Array.isArray(data)) {
      return serializeDict(data, d - 1);
    } else if (Array.isArray(data)) {
      return serializeList(data, d - 1);
    } else {
      return text;
    }
  } catch (e) {
    // Not valid JSON, apply text-level compaction
    return textCompaction(text, d);
  }
}

/**
 * Serialize a dict to ZON format recursively.
 */
function serializeDict(data: Record<string, any>, depth: number): string {
  if (depth <= 0) {
    return JSON.stringify(data, Object.keys(data).length > 0 ? ["", ""] : undefined);
  }

  const parts: string[] = [];
  for (const [k, v] of Object.entries(data)) {
    const compressedValue = compressValue(v, depth - 1);
    parts.push(`${k}:${compressedValue}`);
  }

  return `{${parts.join(",")}}`;
}

/**
 * Serialize a list to ZON format recursively.
 */
function serializeList(data: any[], depth: number): string {
  if (depth <= 0) {
    return JSON.stringify(data);
  }

  const parts: string[] = [];
  for (const item of data) {
    parts.push(compressValue(item, depth - 1));
  }

  return `[${parts.join(",")}]`;
}

/**
 * Compress a value based on its type and depth level.
 */
function compressValue(value: any, depth: number): any {
  if (depth <= 0) return value;

  if (typeof value === "object" && value !== null) {
    if (Array.isArray(value)) {
      return serializeList(value, depth - 1);
    } else {
      return serializeDict(value, depth - 1);
    }
  } else if (typeof value === "string") {
    // Compress string: remove extra whitespace
    const compressed = value.replace(/\s+/g, " ").trim();
    return depth > 2 ? `"${compressed}"` : compressed;
  } else if (typeof value === "boolean") {
    return value ? "true" : "false";
  } else if (typeof value === "number") {
    return String(value);
  } else {
    return JSON.stringify(value);
  }
}

/**
 * Apply text-level ZON compaction for non-JSON content.
 */
function textCompaction(text: string, depth: number): string {
  depth = Math.max(1, Math.min(10, depth));

  // Remove multiple spaces, normalize
  let result = text.replace(/\s+/g, " ").trim();

  // Based on depth, apply different levels of compaction
  if (depth <= 3) {
    // Light compaction: just normalize whitespace
    return result;
  } else if (depth <= 7) {
    // Medium compaction: normalize + remove small filler words
    const fillerPatterns: Array<RegExp> = [
      /\bvery\s+/gi,
      /\breally\s+/gi,
      /\babsolutely\s+/gi,
    ];

    for (const pattern of fillerPatterns) {
      result = result.replace(pattern, "");
    }
    return result;
  } else {
    // Aggressive compaction: normalize + remove fillers + condense code patterns
    result = result.replace(/\bvery\s+/gi, "");
    result = result.replace(/\breally\s+/gi, "");
    result = result.replace(/\babsolutely\s+/gi, "");
    result = result.replace(/for\s+\w+\s+in\s+/g, "for _ in ");
    result = result.replace(/if\s+\w+\s+is\s+/g, "if ");
    result = result.replace(/while\s+\w+\s+is\s+/g, "while ");
    return result;
  }
}

// ============================================================
// Export Types
// ============================================================

export interface TokenMetrics {
  totalTokens: number;
  reducibleTokens: number;
  essentialTokens: number;
  compressionRatio: number;
  qualityScore: number;
  reductionAchieved: number;
  belowThreshold: boolean;
}

export interface ReductionResult {
  originalTokens: number;
  reducedTokens: number;
  remainingTokens: number;
  reductionPercentage: number;
  qualityPercentage: number;
  passedQualityGate: boolean;
  verdict: string;
  zonalFormat: string | null;
  metadata: {
    metrics: {
      totalTokens: number;
      reducibleTokens: number;
      essentialTokens: number;
      compressionRatio: number;
    };
    config: {
      targetReduction: number;
      minimumQuality: number;
      optimizationLevel: string;
      useZon: boolean;
      agentType: string;
    };
  };
}

// Make core reducers available
export {
  countTokensPy,
  analyzeTextPy,
  applyBasicReductionPy,
};