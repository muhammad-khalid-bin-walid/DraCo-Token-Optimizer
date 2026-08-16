/* DraCo Token Optimizer - TypeScript Types
 * Type definitions for the draco-token-optimizer npm package
 */

// ============================================================
// Core Types
// ============================================================

/**
 * Metrics for token analysis and reduction.
 */
export interface TokenMetrics {
  /** Total number of tokens in the text */
  totalTokens: number;
  /** Number of tokens identified as reducible */
  reducibleTokens: number;
  /** Number of tokens identified as essential */
  essentialTokens: number;
  /** Compression ratio (reducible / total) */
  compressionRatio: number;
  /** Quality score (essential / total), 0-1 scale */
  qualityScore: number;
  /** Reduction achievable as percentage */
  reductionAchieved: number;
  /** Whether quality falls below the minimum threshold */
  belowThreshold: boolean;
}

/**
 * Result of a token reduction operation.
 */
export interface ReductionResult {
  /** Original token count */
  originalTokens: number;
  /** Reduced token count */
  reducedTokens: number;
  /** Remaining (reduced) token count */
  remainingTokens: number;
  /** Reduction percentage achieved */
  reductionPercentage: number;
  /** Quality percentage preserved */
  qualityPercentage: number;
  /** Whether the quality gate passed */
  passedQualityGate: boolean;
  /** Verdict string describing the reduction quality */
  verdict: string;
  /** ZON formatted output if ZON encoding was enabled */
  zonalFormat: string | null;
  /** Additional metadata about the reduction */
  metadata: {
    /** Token analysis metrics */
    metrics: {
      totalTokens: number;
      reducibleTokens: number;
      essentialTokens: number;
      compressionRatio: number;
    };
    /** Configuration used for reduction */
    config: {
      /** Target token reduction percentage */
      targetReduction: number;
      /** Minimum quality preservation percentage */
      minimumQuality: number;
      /** Optimization level: conservative, balanced, or maximum */
      optimizationLevel: "conservative" | "balanced" | "maximum";
      /** Whether ZON formatting was applied */
      useZon: boolean;
      /** Target agent type */
      agentType: string;
    };
  };
}

// ============================================================
// Reduction Configuration
// ============================================================

/**
 * Configuration for token reduction operations.
 */
export interface ReductionConfig {
  /** Target token reduction percentage (default: 90) */
  targetReduction?: number;
  /** Minimum quality preservation percentage (default: 90) */
  minimumQuality?: number;
  /** Optimization level: conservative, balanced, or maximum */
  optimizationLevel?: "conservative" | "balanced" | "maximum";
  /** Whether to use ZON formatting */
  useZon?: boolean;
  /** ZON compression depth (1-10, default: 5) */
  zodDepth?: number;
  /** Target agent type for YAGNI ladder */
  agentType?: "claude_code" | "cursor" | "copilot" | "codex" | "auto_detect";
}

// ============================================================
// Verdict Types
// ============================================================

/** Possible verdict outcomes from reduction operations */
export type Verdict =
  | "reduce_tokens"
  | "preserve_quality"
  | "minimal_change"
  | "quality_compromise"
  | "restore_original"
  | "optimize_readability";

/** YAGNI-first decision ladder levels */
export type YagniLevel = 1 | 2 | 3 | 4 | 5 | 6;

/** Optimization levels for the reduction engine */
export type OptimizationLevel = "conservative" | "balanced" | "maximum";

// ============================================================
// Agent Types and YAGNI Levels
// ============================================================

/** Supported AI coding agent types */
export type AgentType =
  | "claude_code"
  | "cursor"
  | "copilot"
  | "codex"
  | "generic_adapter"
  | "auto_detect";

/** Agent YAGNI ladder configuration */
export interface AgentYagniConfig {
  /** YAGNI level (1-6, where 1 is most conservative) */
  yagniLevel: YagniLevel;
  /** Maximum allowed token reduction percentage */
  reductionCap: number;
  /** Minimum quality preservation percentage */
  qualityMinimum: number;
}

/** Predefined agent YAGNI configurations */
export const AGENT_YAGNI_CONFIGS: Record<AgentType, AgentYagniConfig> = {
  claude_code: { yagniLevel: 3, reductionCap: 85, qualityMinimum: 90 },
  cursor: { yagniLevel: 3, reductionCap: 92, qualityMinimum: 90 },
  copilot: { yagniLevel: 3, reductionCap: 88, qualityMinimum: 90 },
  codex: { yagniLevel: 3, reductionCap: 91, qualityMinimum: 90 },
  generic_adapter: { yagniLevel: 4, reductionCap: 95, qualityMinimum: 80 },
  auto_detect: { yagniLevel: 3, reductionCap: 85, qualityMinimum: 90 },
};

// ============================================================
// MCP Protocol Types
// ============================================================

/** MCP message types */
export type McpMessageType =
  | "command"
  | "response"
  | "notification"
  | "event";

/** MCP transport protocols */
export type McpTransport = "stdio" | "http" | "websocket";

/** MCP message payload */
export interface McpPayload {
  /** Message type */
  type: McpMessageType;
  /** Sender identifier */
  sender: string;
  /** Receiver identifier */
  receiver: string;
  /** Message payload data */
  data: unknown;
  /** Correlation ID for tracking */
  correlationId: string;
  /** Timestamp */
  timestamp: string;
}

// ============================================================
// ZON Format Types
// ============================================================

/** ZON compression depth level */
export type ZonDepth = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

/** ZON readability modes */
export type ZonReadabilityMode = "binary-optimized" | "balanced" | "human-readable";

/** ZON serialization result */
export interface ZonResult {
  /** ZON-formatted string */
 zon: string;
  /** Human-readable description of compression achieved */
  description: string;
  /** Percentage reduction vs JSON */
  reductionPercentage: number;
}

// ============================================================
// Continuous Learning Types
// ============================================================

/** Feedback entry from continuous learning loop */
export interface LearningFeedback {
  /** Timestamp of the feedback entry */
  timestamp: string;
  /** Token reduction percentage achieved */
  reductionPercentage: number;
  /** Quality percentage preserved */
  qualityPercentage: number;
  /** Whether quality gate passed */
  passedQualityGate: boolean;
  /** Agent type (if applicable) */
  agentType?: AgentType;
  /** Phase number (if applicable) */
  phaseNumber?: number;
  /** User correction notes */
  notes?: string;
}

/** Heuristic refinement result from CMA-ES */
export interface HeuristicRefinement {
  /** Improved parameters */
  parameters: Record<string, number>;
  /** Expected improvement percentage */
  expectedImprovement: number;
  /** Convergence score (0-1) */
  convergence: number;
  /** Iteration number */
  iteration: number;
}

// ============================================================
// Export All Types
// ============================================================

export {
  TokenMetrics,
  ReductionResult,
  ReductionConfig,
  Verdict,
  YagniLevel,
  OptimizationLevel,
  AgentType,
  AgentYagniConfig,
  McpMessageType,
  McpTransport,
  McpPayload,
  ZonDepth,
  ZonReadabilityMode,
  ZonResult,
  LearningFeedback,
  HeuristicRefinement,
};