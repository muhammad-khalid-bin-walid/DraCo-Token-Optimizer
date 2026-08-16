# DraCo Token Optimizer - Core Subpackage
"""Core module for DraCo token optimizer.

Provides core reduction, formatting, benchmarking, and compression operations.
"""

from .reducer import (
    TokenMetrics,
    ReductionResult,
    CompressionConfig,
    count_tokens,
    analyze_text,
    apply_basic_reduction,
    reduce_tokens_batch,
    get_reduction_summary,
    get_reduction_target,
    get_quality_threshold,
)
from .formatter import (
    FormattingOptions,
    format_verdict_first,
    format_json,
    format_markdown,
    format_batch,
)
from .benchmark import (
    BenchmarkResult,
    BenchmarkSession,
    run_benchmark,
    run_batch_benchmarks,
    compare_benchmarks,
)

__all__ = [
    "TokenMetrics",
    "ReductionResult",
    "CompressionConfig",
    "count_tokens",
    "analyze_text",
    "apply_basic_reduction",
    "reduce_tokens_batch",
    "get_reduction_summary",
    "get_reduction_target",
    "get_quality_threshold",
    "FormattingOptions",
    "format_verdict_first",
    "format_json",
    "format_markdown",
    "format_batch",
    "BenchmarkResult",
    "BenchmarkSession",
    "run_benchmark",
    "run_batch_benchmarks",
    "compare_benchmarks",
]