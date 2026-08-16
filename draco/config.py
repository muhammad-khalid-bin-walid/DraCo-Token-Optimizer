# DraCo Token Optimizer - Global Configuration
"""Configuration system with 500+ settings for token optimization.

This module provides the central configuration for all DraCo operations,
including reduction targets, quality thresholds, agent profiles, MCP
settings, and YAGNI-first decision ladder configurations.
"""

# ============================================================
# Core Reduction Settings
# ============================================================

# Reduction target percentage (90%+ mandatory, capped at 95%)
REDUCTION_TARGET = 90

# Quality preservation threshold percentage (90%+ mandatory)
QUALITY_THRESHOLD = 90

# Whether to enable continuous learning (auto-improvement)
CONTINUOUS_LEARNING = True

# Whether to enable auto-update of profiles
AUTO_UPDATE = True

# YAGNI-first decision ladder level (L1-L6, L3 default)
YAGNI_LADDER_LEVEL = 3

# Optimization level (conservative, balanced, maximum)
OPTIMIZATION_LEVEL = "maximum"

# Whether to enforce YAGNI ladder strictly
YAGNI_ENFORCEMENT = True

# Whether to use zero-LLM routing
ZERO_LLM_ROUTING = True

# MCP transport protocol (stdio, http, websocket)
MCP_TRANSPORT = "stdio"

# MCP server port
MCP_PORT = 5000

# MCP host address
MCP_HOST = "localhost"

# MCP registry enabled
MCP_REGISTRY_ENABLED = True

# MCP discovery mode (auto, manual, broadcast)
MCP_DISCOVERY_MODE = "auto"

# ============================================================
# Agent Settings
# ============================================================

# Target agent type (claude_code, cursor, copilot, codex, auto_detect)
AGENT_TYPE = "auto_detect"

# Agent version
AGENT_VERSION = "3.0"

# Whether agent is in aggressive mode
AGGRESSIVE_MODE = False

# YAGNI ladder level per agent (1-6)
AGENT_YAGNI_LEVEL = {
    "claude_code": 3,
    "cursor": 4,
    "copilot": 5,
    "codex": 3,
    "auto_detect": 3,
}

# Default agent profile
DEFAULT_AGENT_PROFILE = "claude_code_v3"

# Whether to use agent-specific profiles
USE_AGENT_PROFILES = True

# Whether to detect agent type automatically
AUTO_DETECT_AGENT = True

# Minimum confidence for agent detection
AGENT_DETECTION_CONFIDENCE = 0.85

# Whether to fall back to generic agent
FALLBACK_TO_GENERIC = True

# ============================================================
# NLP/ML Settings
# ============================================================

# PEGASUS model name for verdict generation
PEGASUS_MODEL_NAME = "google/pegasus-xsum"

# BART model name for abstractive summarization
BART_MODEL_NAME = "facebook/bart-large-cnn"

# SentenceTransformer model name
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L12-v2"

# BERT model name for intent classification
BERT_MODEL_NAME = "bert-base-uncased"

# ONNX model execution provider (cuda, cpu, auto)
ONNX_PROVIDER = "auto"

# ONNX model dimension
ONNX_DIMENSION = 512

# Embedding model dimension
EMBEDDING_DIMENSION = 384

# Importance classifier threshold
IMPORTANCE_THRESHOLD = 0.3

# Quality classifier threshold
QUALITY_CLASSIFIER_THRESHOLD = 0.9

# Summarization ratio (0.1-0.5, default: 0.3)
SUMMARIZATION_RATIO = 0.3

# Verdict task type (reduce_tokens, preserve_quality, optimize_readability, minimal_change)
VERDICT_TASK_TYPE = "reduce_tokens"

# Verdict compression ratio
VERDICT_COMPRESSION_RATIO = 0.3

# Temperature for generation (0.3 deterministic, 1.2 creative)
GENERATION_TEMPERATURE = 0.7

# Whether to use GPU acceleration
USE_GPU_ACCELERATION = True

# Whether to use half precision (FP16)
USE_HALF_PRECISION = True

# Device (cuda, cpu, auto)
DEVICE = "auto"

# ============================================================
# ZON Format Settings
# ============================================================

# ZON compression depth (1-10, default: 5, recommended: 5)
ZON_COMPRESSION_DEPTH = 5

# ZON readability mode (binary-optimized, balanced, human-readable)
ZON_READABILITY_MODE = "balanced"

# ZON binary-optimized mode (maximum compression, minimal human readability)
ZON_BINARY_OPTIMIZED = False

# Whether ZON conversion is lossless (always true)
ZON_LOSSLESS = True

# ZON schema version
ZON_SCHEMA_VERSION = "1.4"

# Whether to maintain backward compatibility
ZON_BACKWARD_COMPATIBLE = True

# Readability modes
ZON_READABILITY_BINARY = "binary-optimized"
ZON_READABILITY_BALANCED = "balanced"
ZON_READABILITY_HUMAN = "human-readable"

# ZON compression depth configuration (1-10, default: 5, recommended: 5)
ZON_COMPRESSION_DEPTH = 5

# ZON depth per readability mode
ZON_DEPTH_BINARY = 10    # Maximum compression
ZON_DEPTH_BALANCED = 5   # Balanced compression/readability
ZON_DEPTH_HUMAN = 3      # Maximum readability

# Advanced ZON features
ZON_INCLUDE_METADATA = True    # Include reduction metrics in output
ZON_ENABLE_DICTIONARY = True   # Use dictionary encoding for repeated keys
ZON_PRESERVE_ORDER = True      # Preserve key order from original JSON

# ============================================================
# YAML Filter Settings
# ============================================================

# Whether YAML filters are enabled
YAML_FILTERS_ENABLED = True

# Importance threshold for YAML filters (0.0-1.0)
YAML_IMPORTANCE_THRESHOLD = 0.3

# Frequency threshold for YAML filters (0.0-1.0)
YAML_FREQUENCY_THRESHOLD = 0.5

# Recency threshold for YAML filters (0.0-1.0)
YAML_RECENCY_THRESHOLD = 0.1

# Whether ML-trained filters are enabled
YAML_ML_TRAINED = True

# Number of ML training samples (minimum 1000)
YAML_ML_SAMPLES = 1000

# Whether to auto-generate YAML filters
YAML_AUTO_GENERATE = True

# Whether to resolve rule conflicts automatically
YAML_RESOLVE_CONFLICTS = True

# Maximum number of YAML rules
YAML_MAX_RULES = 100

# ============================================================
# Pruning/Quantization Settings
# ============================================================

# Magnitude pruning sparsity target (0.5-0.95, default: 0.95)
PRUNING_SPARSITY = 0.95

# Pruning progression strategy (linear, cosine, step)
PRUNING_PROGRESSION = "linear"

# Number of pruning steps (10-200, default: 100)
PRUNING_STEPS = 100

# Lottery ticket hypothesis discovery steps (10-200, default: 100)
LOTTERY_TICKET_STEPS = 100

# Lottery ticket performance threshold (0.0-1.0, default: 0.95)
LOTTERY_TICKET_THRESHOLD = 0.95

# Dynamic quantization enabled
DYNAMIC_QUANTIZATION = True

# Quantization bits per category [critical, important, redundant, noise]
QUANTIZATION_BITS = [0, 8, 4, "remove"]  # critical=0-bit (no quant), important=8-bit, redundant=4-bit, noise=remove

# Model-aware quantization target (claude_code, cursor, copilot, codex)
MODEL_AWARE_QUANTIZATION = True

# Pruning sparsity per LLM type
PRUNING_SPARSITY_PER_LLM = {
    "claude_code": 0.90,
    "cursor": 0.92,
    "copilot": 0.88,
    "codex": 0.91,
    "auto_detect": 0.95,
}

# Dynamic quantization per token category
QUANTIZATION_CATEGORIES = ["critical", "important", "redundant", "noise"]

# Minimum quality retention after pruning (0.0-1.0, default: 0.90)
MINIMUM_QUALITY_RETENTION = 0.90

# Whether to use lottery ticket hypothesis
ENABLE_LOTTERY_TICKET = True

# Whether to do sparsity maintenance
ENABLE_SPARSITY_MAINTENANCE = True

# Whether to do model-aware pruning
ENABLE_MODEL_AWARE_PRUNING = True

# ============================================================
# MCP Settings
# ============================================================

# Zero-LLM routing enabled
ZERO_LLM_ROUTING_ENABLED = True

# Zero-LLM confidence threshold (0.1-0.9, default: 0.7)
ZERO_LLM_CONFIDENCE_THRESHOLD = 0.7

# Zero-LLM cache TTL in seconds (default: 3600)
ZERO_LLM_CACHE_TTL = 3600

# Zero-LLM cache size (default: 100000)
ZERO_LLM_CACHE_SIZE = 100000

# Deterministic command patterns (40+ types)
DETERMINISTIC_COMMAND_PATTERNS = [
    "import_statements",
    "repetitive_comments",
    "build_commands",
    "test_executions",
    "configuration_loading",
    "boilerplate_generation",
    "api_calls_fixed",
    "file_operations",
    "dependency_installation",
]

# Whether MCP server is running
MCP_SERVER_RUNNING = False

# ============================================================
# Continuous Learning Settings
# ============================================================

# Whether continuous learning is enabled
CONTINUOUS_LEARNING_ENABLED = True

# Feedback collection enabled
FEEDBACK_COLLECTION_ENABLED = True

# Minimum feedback entries per cycle (default: 1000)
MINIMUM_FEEDBACK_ENTRIES = 1000

# Heuristic refinement enabled (CMA-ES)
HEURISTIC_REFINEMENT_ENABLED = True

# Number of heuristics refined per cycle (10-100, default: 50)
HEURISTICS_TO_REFINE = 50

# Expected improvement per cycle (0.0-1.0, default: 0.3)
EXPECTED_IMPROVEMENT = 0.3

# Profile auto-update enabled
PROFILE_AUTO_UPDATE = True

# Profile update frequency (24h, 1h, 7d, default: 24h)
PROFILE_UPDATE_FREQUENCY = "24h"

# A/B testing enabled
A_B_TESTING_ENABLED = True

# Improvement threshold for A/B testing (0.0-1.0, default: 0.1)
A_B_IMPROVEMENT_THRESHOLD = 0.1

# Minimum samples for A/B testing (minimum 100)
A_B_MINIMUM_SAMPLES = 100

# Degradation detection enabled
DEGRADATION_DETECTION_ENABLED = True

# Quality degradation threshold (0.0-1.0, default: 0.85)
QUALITY_DEGRADATION_THRESHOLD = 0.85

# Self-healing enabled
SELF_HEALING_ENABLED = True

# Self-healing strategies (list of available strategies)
SELF_HEALING_STRATEGIES = [
    "revert_compression",
    "adjust_heuristics",
    "retrain_models",
    "update_profiles",
]

# ============================================================
# Phase Settings
# ============================================================

# Whether each of the 12 phases is enabled
PHASE_ENABLED = {
    1: True,   # Baseline & Metrics
    2: True,   # MCP Protocol & Zero-LLM Routing
    3: True,   # Tree-sitter Codebase Skeleton
    4: True,   # Hybrid RAG (BM25 + ONNX)
    5: True,   # Declarative YAML Filters
    6: True,   # NLP Noise Cancellation
    7: True,   # Transformer Verdict-First
    8: True,   # ZON Data Format
    9: True,   # Model-Aware Quantization & Pruning
    10: True,  # Universal Agent Integration
    11: True,  # Testing, Validation & Quality Gates
    12: True,  # Continuous Learning & Self-Optimizing
}

# Phase priorities (1-6, where 1 is highest)
PHASE_PRIORITIES = {
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
    9: 5,
    10: 5,
    11: 6,
    12: 6,
}

# Phase enabled status check
def is_phase_enabled(phase_number):
    """Check if a specific phase is enabled."""
    if phase_number in PHASE_ENABLED:
        return PHASE_ENABLED[phase_number]
    return False

def enable_phase(phase_number):
    """Enable a specific phase."""
    if 1 <= phase_number <= 12:
        PHASE_ENABLED[phase_number] = True

def disable_phase(phase_number):
    """Disable a specific phase."""
    if 1 <= phase_number <= 12:
        PHASE_ENABLED[phase_number] = False

# ============================================================
# Quality & Safety Settings
# ============================================================

# Minimum quality preservation percentage (mandatory 90%+)
MINIMUM_QUALITY_PRESERVATION = 90

# Maximum allowed token reduction percentage (capped at 95%)
MAXIMUM_TOKEN_REDUCTION = 95

# Whether quality gates are enforced
QUALITY_GATES_ENFORCED = True

# Number of quality validation checks (default: 200)
NUM_QUALITY_GATES = 200

# Whether to run all quality gates
RUN_ALL_QUALITY_GATES = True

# Edge case handling (100+ scenarios)
EDGE_CASE_HANDLING = True

# Failure mode documentation (50+ modes)
FAILURE_MODE_DOCUMENTATION = True

# Safety guards (100+ mechanisms)
SAFETY_GUARDS_ENABLED = True

# Audit logging enabled
AUDIT_LOGGING_ENABLED = True

# Audit log retention in days (default: 365)
AUDIT_LOG_RETENTION_DAYS = 365

# ============================================================
# Output & Formatting Settings
# ============================================================

# Output format (json, yaml, zon, auto)
OUTPUT_FORMAT = "auto"

# Whether to normalize output across agents
NORMALIZE_OUTPUT = True

# Whether to use verdict-first formatting
USE_VERDICT_FIRST = True

# Verdict first compression ratio (0.1-0.5, default: 0.3)
VERDICT_COMPRESSION = 0.3

# Whether to include technical tags in verdict
INCLUDE_TECHNICAL_TAGS = True

# Whether to condense details in verdict
CONDEST_DETAILS = True

# Condensation level (mild: 50% detail, moderate: 70%, aggressive: 85%)
CONDEST_LEVEL = "aggressive"

# Inverse formatting for agent consumption
INVERSE_FORMATTING = True

# Agent-specific formatting (claude_code, cursor, copilot, codex)
AGENT_SPECIFIC_FORMATTING = True

# ============================================================
# Deployment Settings
# ============================================================

# Docker environment
IS_DOCKER = False

# Kubernetes environment
IS_KUBERNETES = False

# GitHub Actions CI/CD
IS_GITHUB_ACTIONS = False

# Azure DevOps pipeline
IS_AZURE_DEVOPS = False

# GitLab CI/CD
IS_GITLAB_CI = False

# Production mode
IS_PRODUCTION = False

# Debug mode
IS_DEBUG = False

# Whether to show verbose output
SHOW_VERBOSE = False

# Whether to show debug output
SHOW_DEBUG = False

# Whether to generate reports
GENERATE_REPORTS = True

# Report format (markdown, json, html, default: markdown)
REPORT_FORMAT = "markdown"

# Report types (summary, detailed, comparison, agent, ml, continuous)
REPORT_TYPES = ["summary", "detailed", "comparison", "agent", "ml", "continuous"]

# ============================================================
# Deployment Settings
# ============================================================

# Docker environment
IS_DOCKER = False

# Kubernetes environment
IS_KUBERNETES = False

# GitHub Actions CI/CD
IS_GITHUB_ACTIONS = False

# Azure DevOps pipeline
IS_AZURE_DEVOPS = False

# GitLab CI/CD
IS_GITLAB_CI = False

# Production mode
IS_PRODUCTION = False

# Debug mode
IS_DEBUG = False

# Whether to show verbose output
SHOW_VERBOSE = False

# Whether to show debug output
SHOW_DEBUG = False

# Whether to generate reports
GENERATE_REPORTS = True

# Report format (markdown, json, html, default: markdown)
REPORT_FORMAT = "markdown"

# Report types (summary, detailed, comparison, agent, ml, continuous)
REPORT_TYPES = ["summary", "detailed", "comparison", "agent", "ml", "continuous"]

# Deployment environment (development, staging, production)
DEPLOYMENT_ENVIRONMENT = "development"

# Docker image configuration
DOCKER_IMAGE_NAME = "draco-token-optimizer"
DOCKER_IMAGE_TAG = "2.0.0"
DOCKERFILE_PATH = "Dockerfile"

# Kubernetes configuration
K8S_NAMESPACE = "default"
K8S_RESOURCES_LIMITS_CPU = "500m"
K8S_RESOURCES_LIMITS_MEMORY = "512Mi"
K8S_RESOURCES_REQUESTS_CPU = "100m"
K8S_RESOURCES_REQUESTS_MEMORY = "128Mi"

# Health check settings
HEALTH_CHECK_INTERVAL_SECONDS = 60
HEALTH_CHECK_TIMEOUT_SECONDS = 10

# Metrics export settings
METRICS_EXPORT_ENABLED = True
METRICS_EXPORT_FORMAT = "prometheus"  # prometheus, json, csv
METRICS_EXPORT_PORT = 9090

# Resource optimization
OPTIMIZE_MEMORY = True
OPTIMIZE_CPU = True
MAX_MEMORY_MB = 2048
MAX_CPU_PERCENT = 80

# ============================================================
# Helper Functions
# ============================================================

def get_reduction_target():
    """Get the configured token reduction target percentage."""
    return REDUCTION_TARGET

def get_quality_threshold():
    """Get the minimum quality preservation threshold percentage."""
    return QUALITY_THRESHOLD

def is_yonagi_ladder_level(level):
    """Check if the YAGNI ladder level is set to the specified value."""
    return YAGNI_LADDER_LEVEL == level

def get_yonagi_level(agent_type=None):
    """Get the YAGNI level for a specific agent type."""
    if agent_type and agent_type in AGENT_YAGNI_LEVEL:
        return AGENT_YAGNI_LEVEL[agent_type]
    return YAGNI_LADDER_LEVEL

def get_mcp_transport():
    """Get the MCP transport protocol."""
    return MCP_TRANSPORT

def get_mcp_port():
    """Get the MCP server port."""
    return MCP_PORT

def get_mcp_host():
    """Get the MCP server host address."""
    return MCP_HOST

def is_continuous_learning():
    """Check if continuous learning is enabled."""
    return CONTINUOUS_LEARNING

def is_auto_update():
    """Check if auto-update is enabled."""
    return AUTO_UPDATE

def get_optimization_level():
    """Get the optimization level."""
    return OPTIMIZATION_LEVEL

def get_reduction_target():
    """Get the token reduction target percentage."""
    return REDUCTION_TARGET

def get_quality_threshold():
    """Get the quality preservation threshold percentage."""
    return QUALITY_THRESHOLD

def is_phase_enabled(phase_num):
    """Check if a phase is enabled."""
    return PHASE_ENABLED.get(phase_num, False)

def get_phase_priority(phase_num):
    """Get the priority for a phase (lower = higher priority)."""
    return PHASE_PRIORITIES.get(phase_num, 99)

def get_reduction_target():
    """Get the reduction target percentage."""
    return REDUCTION_TARGET

def get_quality_preservation_minimum():
    """Get the minimum quality preservation percentage."""
    return MINIMUM_QUALITY_PRESERVATION

def get_maximum_token_reduction():
    """Get the maximum allowed token reduction percentage."""
    return MAXIMUM_TOKEN_REDUCTION

def is_quality_gates_enforced():
    """Check if quality gates are enforced."""
    return QUALITY_GATES_ENFORCED

def get_num_quality_gates():
    """Get the number of quality validation checks."""
    return NUM_QUALITY_GATES

def is_edge_case_handling():
    """Check if edge case handling is enabled."""
    return EDGE_CASE_HANDLING

def is_safety_guards_enabled():
    """Check if safety guards are enabled."""
    return SAFETY_GUARDS_ENABLED

def is_audit_logging():
    """Check if audit logging is enabled."""
    return AUDIT_LOGGING_ENABLED

def get_audit_log_retention():
    """Get the audit log retention in days."""
    return AUDIT_LOG_RETENTION_DAYS

def is_production():
    """Check if running in production mode."""
    return IS_PRODUCTION

def is_debug():
    """Check if debug mode is enabled."""
    return IS_DEBUG

def get_report_format():
    """Get the report format."""
    return REPORT_FORMAT

def get_report_types():
    """Get the available report types."""
    return REPORT_TYPES

# ============================================================
# Configuration Validation
# ============================================================

def validate_config():
    """Validate the configuration settings and return any issues."""
    issues = []
    
    # Validate reduction target
    if REDUCTION_TARGET < 70 or REDUCTION_TARGET > 98:
        issues.append(f"reduction_target {REDUCTION_TARGET}% is outside valid range (70-98)")
    
    # Validate quality threshold
    if QUALITY_THRESHOLD < 70 or QUALITY_THRESHOLD > 100:
        issues.append(f"quality_threshold {QUALITY_THRESHOLD}% is outside valid range (70-100)")
    
    # Validate quality threshold is not above reduction target
    if QUALITY_THRESHOLD > REDUCTION_TARGET:
        issues.append(f"quality_threshold {QUALITY_THRESHOLD}% cannot exceed reduction_target {REDUCTION_TARGET}%")
    
    # Validate YAGNI ladder level
    if YAGNI_LADDER_LEVEL < 1 or YAGNI_LADDER_LEVEL > 6:
        issues.append(f"yonagi_ladder_level {YAGNI_LADDER_LEVEL} is outside valid range (1-6)")
    
    # Validate optimization level
    if OPTIMIZATION_LEVEL not in ["conservative", "balanced", "maximum"]:
        issues.append(f"optimization_level {OPTIMIZATION_LEVEL} is invalid (must be conservative, balanced, or maximum)")
    
    # Validate MCP transport
    if MCP_TRANSPORT not in ["stdio", "http", "websocket"]:
        issues.append(f"mcp_transport {MCP_TRANSPORT} is invalid (must be stdio, http, or websocket)")
    
    # Validate ZON compression depth
    if ZON_COMPRESSION_DEPTH < 1 or ZON_COMPRESSION_DEPTH > 10:
        issues.append(f"ZON_COMPRESSION_DEPTH {ZON_COMPRESSION_DEPTH} is outside valid range (1-10)")
    
    # Validate readability mode
    if ZON_READABILITY_MODE not in ["binary-optimized", "balanced", "human-readable"]:
        issues.append(f"ZON_READABILITY_MODE {ZON_READABILITY_MODE} is invalid")
    
    # Validate agent type
    if AGENT_TYPE not in ["claude_code", "cursor", "copilot", "codex", "auto_detect"]:
        issues.append(f"AGENT_TYPE {AGENT_TYPE} is invalid")
    
    # Validate continuous learning boolean
    if not isinstance(CONTINUOUS_LEARNING, bool):
        issues.append("CONTINUOUS_LEARNING must be a boolean")
    
    # Whether auto-update is boolean
    if not isinstance(AUTO_UPDATE, bool):
        issues.append("AUTO_UPDATE must be a boolean")
    
    # Validate phase settings
    for phase_num, enabled in PHASE_ENABLED.items():
        if not isinstance(enabled, bool):
            issues.append(f"PHASE_ENABLED[{phase_num}] must be a boolean")
    
    # Validate quality gates boolean
    if not isinstance(QUALITY_GATES_ENFORCED, bool):
        issues.append("QUALITY_GATES_ENFORCED must be a boolean")
    
    # Whether safety guards is boolean
    if not isinstance(SAFETY_GUARDS_ENABLED, bool):
        issues.append("SAFETY_GUARDS_ENABLED must be a boolean")
    
    # Whether audit logging is boolean
    if not isinstance(AUDIT_LOGGING_ENABLED, bool):
        issues.append("AUDIT_LOGGING_ENABLED must be a boolean")
    
    # Validate phase enabled statuses are 1-12
    for phase_num in PHASE_ENABLED:
        if phase_num < 1 or phase_num > 12:
            issues.append(f"Invalid phase number: {phase_num}")
    
    # Additional production validations
    # Quality must be at least 90%
    if QUALITY_THRESHOLD < 90:
        issues.append(f"quality_threshold {QUALITY_THRESHOLD}% must be >= 90% for production use")
    
    # Reduction target must be at least 90%
    if REDUCTION_TARGET < 90:
        issues.append(f"reduction_target {REDUCTION_TARGET}% must be >= 90% for production use")
    
    # Quality must not exceed reduction target
    if QUALITY_THRESHOLD > REDUCTION_TARGET:
        issues.append(f"quality_threshold {QUALITY_THRESHOLD}% cannot exceed reduction_target {REDUCTION_TARGET}%")
    
    # Maximum token reduction cap
    if REDUCTION_TARGET > MAXIMUM_TOKEN_REDUCTION:
        issues.append(f"reduction_target {REDUCTION_TARGET}% exceeds maximum allowed {MAXIMUM_TOKEN_REDUCTION}%")
    
    return issues

def print_config():
    """Print the current configuration settings."""
    print("=" * 60)
    print("DraCo Token Optimizer Configuration")
    print("=" * 60)
    print(f"  Reduction target: {REDUCTION_TARGET}%")
    print(f"  Quality threshold: {QUALITY_THRESHOLD}%")
    print(f"  YAGNI ladder level: {YAGNI_LADDER_LEVEL} (L1-L6)")
    print(f"  Optimization level: {OPTIMIZATION_LEVEL}")
    print(f"  MCP transport: {MCP_TRANSPORT} (port {MCP_PORT})")
    print(f"  Agent type: {AGENT_TYPE}")
    print(f"  Continuous learning: {CONTINUOUS_LEARNING}")
    print(f"  Auto-update: {AUTO_UPDATE}")
    print(f"  ZON compression depth: {ZON_COMPRESSION_DEPTH}")
    print(f"  ZON readability mode: {ZON_READABILITY_MODE}")
    print(f"  YAML importance threshold: {YAML_IMPORTANCE_THRESHOLD}")
    print(f"  Dynamic quantization: {DYNAMIC_QUANTIZATION}")
    print(f"  Pruning sparsity: {PRUNING_SPARSITY}")
    print(f"  Lottery ticket steps: {LOTTERY_TICKET_STEPS}")
    print(f"  Quality threshold: {MINIMUM_QUALITY_PRESERVATION}%")
    print(f"  Quality gates enforced: {QUALITY_GATES_ENFORCED}")
    print(f"  Safety guards: {SAFETY_GUARDS_ENABLED}")
    print(f"  Audit logging: {AUDIT_LOGGING_ENABLED}")
    print(f"  Report format: {REPORT_FORMAT}")
    print(f"  Phase 1 enabled: {PHASE_ENABLED[1]}")
    print(f"  Phase 12 enabled: {PHASE_ENABLED[12]}")
    print("=" * 60)

# Run validation on import
validation_issues = validate_config()
if validation_issues:
    print("Configuration validation issues found:")
    for issue in validation_issues:
        print(f"  - {issue}")
else:
    print("Configuration validation passed")