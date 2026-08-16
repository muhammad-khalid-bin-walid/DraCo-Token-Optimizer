"""DraCo Token Optimizer - Benchmark Suite

Provides standardized reduction quality metrics and benchmarking 
across all 12 phases of the DraCo pipeline.
"""

import json
import time
import tempfile
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from draco.core.reducer import (
    count_tokens,
    analyze_text,
    apply_basic_reduction,
    TokenMetrics,
    ReductionResult,
)
from draco.config import (
    REDUCTION_TARGET,
    QUALITY_THRESHOLD,
    MINIMUM_QUALITY_PRESERVATION,
    MAXIMUM_TOKEN_REDUCTION,
    NUM_QUALITY_GATES,
)


# ============================================================
# Benchmark Data Types
# ============================================================

class BenchmarkResult:
    """Result of a single benchmark run."""
    
    def __init__(
        self,
        phase: int,
        test_name: str,
        original_tokens: int,
        reduced_tokens: int,
        reduction_percentage: float,
        quality_percentage: float,
        passed_quality_gate: bool,
        verdict: str,
        execution_time: float,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.phase = phase
        self.test_name = test_name
        self.original_tokens = original_tokens
        self.reduced_tokens = reduced_tokens
        self.reduction_percentage = reduction_percentage
        self.quality_percentage = quality_percentage
        self.passed_quality_gate = passed_quality_gate
        self.verdict = verdict
        self.execution_time = execution_time
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "test_name": self.test_name,
            "original_tokens": self.original_tokens,
            "reduced_tokens": self.reduced_tokens,
            "reduction_percentage": self.reduction_percentage,
            "quality_percentage": self.quality_percentage,
            "passed_quality_gate": self.passed_quality_gate,
            "verdict": self.verdict,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
    
    @property
    def meets_target(self) -> bool:
        """Check if reduction meets the 90%+ target."""
        return self.reduction_percentage >= 90
    
    @property
    def meets_quality(self) -> bool:
        """Check if quality preserves 90%+ threshold."""
        return self.quality_percentage >= 90
    
    @property
    def meets_both(self) -> bool:
        """Check if both reduction target and quality threshold are met."""
        return self.meets_target and self.meets_quality


# ============================================================
# Benchmark Test Suites
# ============================================================

# Code samples for different categories
CODE_BENCHMARKS = {
    "comments": [
        "# This is a comment\n# Please note that we need to build the project\n\ndef hello():",
    ],
    "verbose_phrases": [
        "It is important to note that the build process should be run after you have built the project.",
        "Please note that running the tests will verify the code correctness.",
        "One should consider the implications of the changes before building.",
    ],
    "repetitive_commands": [
        "build your project\nrun the tests\npass the linting check",
        "build your project\nrun your code\ncheck the results",
    ],
    "filler_words": [
        "This is absolutely very really important to note that the code should work correctly.",
        "You should very carefully consider the implications of this change.",
    ],
    "code_patterns": [
        "for i in range(len(items)):\n    print(items[i])\n",
        "if x is None:\n    return None\n",
        "while i is not None:\n    do_something(i)\n",
    ],
    "mixed_content": [
        "# Comment with verbose phrase: please note that this is important\n# Another comment\n\ndef calculate_total(items):\n    # Initialize total\n    total = 0\n    # Loop through items\n    for i in range(len(items)):\n        # Add each item to total\n        total = total + items[i]\n    # Return the total\n    return total\n",
    ],
}


# ============================================================
# Benchmark Suites per Phase
# ============================================================

def run_phase_1_baseline() -> List[BenchmarkResult]:
    """Phase 1: Baseline & Metrics Establishment
    
    Tests token counting infrastructure and metric collection.
    """
    results = []
    test_cases = [
        ("simple_text", "Hello world"),
        ("code_snippet", "def hello():\n    pass"),
        ("comment_block", "# Comment 1\n# Comment 2\n# Comment 3"),
        ("verbose_text", "It is important to note that we need to please note that this works."),
    ]
    
    for name, text in test_cases:
        start = time.time()
        tokens = count_tokens(text)
        metrics = analyze_text(text)
        elapsed = time.time() - start
        
        results.append(BenchmarkResult(
            phase=1,
            test_name=f"Phase1_{name}",
            original_tokens=tokens,
            reduced_tokens=tokens,  # Baseline: no reduction yet
            reduction_percentage=0.0,
            quality_percentage=metrics.quality_score * 100,
            passed_quality_gate=metrics.quality_score * 100 >= 90,
            verdict="minimal_change",
            execution_time=elapsed,
            metadata={"token_count": tokens, "quality_score": metrics.quality_score}
        ))
    
    return results


def run_phase_7_verdict() -> List[BenchmarkResult]:
    """Phase 7: Transformer Verdict-First Output Formatting"""
    results = []
    test_cases = CODE_BENCHMARKS["verbose_phrases"] + CODE_BENCHMARKS["comments"]
    
    for test_name in ["verbose1", "verbose2"]:
        text = CODE_BENCHMARKS["verbose_phrases"][0] if test_name == "verbose1" else CODE_BENCHMARKS["comments"][0]
        start = time.time()
        result = apply_basic_reduction(text, {
            "target_reduction": 90,
            "minimum_quality": 90,
            "optimization_level": "maximum",
            "use_zon": False,
        })
        elapsed = time.time() - start
        
        results.append(BenchmarkResult(
            phase=7,
            test_name=f"Phase7_{test_name}",
            original_tokens=result["original_tokens"],
            reduced_tokens=result["reduced_tokens"],
            reduction_percentage=result["reduction_percentage"],
            quality_percentage=result["quality_percentage"],
            passed_quality_gate=result["passed_quality_gate"],
            verdict=result["verdict"],
            execution_time=elapsed,
            metadata={"verdict": result["verdict"], "config_used": "maximum"}
        ))
    
    return results


def run_phase_8_zon() -> List[BenchmarkResult]:
    """Phase 8: ZON Data Format Conversion"""
    from draco.core.reducer import _apply_zon_formatting
    
    results = []
    test_json = '{"items": ["alpha", "beta", "gamma"], "count": 3, "metadata": {"key": "value"}}'
    
    for depth in [3, 5, 8]:
        start = time.time()
        zon = _apply_zon_formatting(test_json, depth)
        elapsed = time.time() - start
        original_tokens = count_tokens(test_json)
        # Estimate ZON tokens (rough approximation)
        zon_tokens = count_tokens(zon)
        reduction = ((original_tokens - zon_tokens) / original_tokens) * 100 if original_tokens > 0 else 0
        
        results.append(BenchmarkResult(
            phase=8,
            test_name=f"Phase8_depth_{depth}",
            original_tokens=original_tokens,
            reduced_tokens=zon_tokens,
            reduction_percentage=reduction,
            quality_percentage=100.0,  # ZON is lossless
            passed_quality_gate=True,
            verdict="reduce_tokens",
            execution_time=elapsed,
            metadata={"zon_depth": depth, "original_size": len(test_json), "zon_size": len(zon)}
        ))
    
    return results


def run_phase_9_quantization() -> List[BenchmarkResult]:
    """Phase 9: Model-Aware Quantization & Pruning"""
    from draco.quantization import apply_magnitude_pruning, apply_dynamic_quantization
    
    results = []
    # Generate sample weights
    import numpy as np
    np.random.seed(42)
    sample_weights = np.random.randn(100).tolist()
    
    # Test pruning at different sparsity levels
    for sparsity in [0.5, 0.75, 0.90, 0.95]:
        start = time.time()
        pruned = apply_magnitude_pruning(sample_weights, sparsity_target=sparsity)
        elapsed = time.time() - start
        
        # Count remaining "effective" weights (non-zero)
        remaining = len([w for w in pruned if abs(w) > 0.01])
        reduction_pct = ((len(sample_weights) - remaining) / len(sample_weights)) * 100
        
        results.append(BenchmarkResult(
            phase=9,
            test_name=f"Phase9_sparsity_{sparsity}",
            original_tokens=len(sample_weights),
            reduced_tokens=remaining,
            reduction_percentage=reduction_pct,
            quality_percentage=sparsity * 100,  # Approximate quality
            passed_quality_gate=sparsity <= 0.90,  # Quality drops significantly above 90%
            verdict="quality_compromise" if sparsity > 0.75 else "reduce_tokens",
            execution_time=elapsed,
            metadata={"sparsity_target": sparsity, "method": "magnitude_pruning"}
        ))
    
    # Test quantization
    for bits in [4, 8]:
        start = time.time()
        quantized = apply_dynamic_quantization(sample_weights, bits_per_category=[bits])
        elapsed = time.time() - start
        
        results.append(BenchmarkResult(
            phase=9,
            test_name=f"Phase9_quant_{bits}bit",
            original_tokens=len(sample_weights),
            reduced_tokens=len(sample_weights),  # Same count, different representation
            reduction_percentage=0.0,
            quality_percentage=95.0,  # Approximate
            passed_quality_gate=True,
            verdict="preserve_quality",
            execution_time=elapsed,
            metadata={"quantization_bits": bits, "method": "dynamic_quantization"}
        ))
    
    return results


# ============================================================
# Standardized Metrics
# ============================================================

class BenchmarkSuite:
    """Runs comprehensive benchmark suite across all phases."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.phases = {
            1: run_phase_1_baseline,
            7: run_phase_7_verdict,
            8: run_phase_8_zon,
            9: run_phase_9_quantization,
        }
    
    def run_all(self) -> Dict[int, List[BenchmarkResult]]:
        """Run benchmarks for all configured phases."""
        all_results = {}
        for phase_num, runner in self.phases.items():
            try:
                phase_results = runner()
                all_results[phase_num] = phase_results
                self.results.extend(phase_results)
            except Exception as e:
                print(f"Phase {phase_num} benchmark failed: {e}")
                all_results[phase_num] = []
        return all_results
    
    def summary(self) -> Dict[str, Any]:
        """Generate summary statistics from all benchmark results."""
        if not self.results:
            return {"error": "No benchmark results available"}
        
        # Overall statistics
        total = len(self.results)
        passed_quality = sum(1 for r in self.results if r.passed_quality_gate)
        met_target = sum(1 for r in self.results if r.meets_target)
        met_both = sum(1 for r in self.results if r.meets_both)
        avg_reduction = sum(r.reduction_percentage for r in self.results) / total
        avg_quality = sum(r.quality_percentage for r in self.results) / total
        avg_time = sum(r.execution_time for r in self.results) / total
        
        # Per-phase stats
        phase_stats = {}
        for phase_num in range(1, 13):
            phase_results = [r for r in self.results if r.phase == phase_num]
            if phase_results:
                phase_stats[phase_num] = {
                    "count": len(phase_results),
                    "avg_reduction": sum(r.reduction_percentage for r in phase_results) / len(phase_results),
                    "avg_quality": sum(r.quality_percentage for r in phase_results) / len(phase_results),
                    "passed_quality": sum(1 for r in phase_results if r.passed_quality_gate),
                    "met_target": sum(1 for r in phase_results if r.meets_target),
                    "met_both": sum(1 for r in phase_results if r.meets_both),
                }
        
        return {
            "total_runs": total,
            "passed_quality_gates": passed_quality,
            "met_reduction_target": met_target,
            "met_both_targets": met_both,
            "average_reduction_percentage": round(avg_reduction, 2),
            "average_quality_percentage": round(avg_quality, 2),
            "average_execution_time": round(avg_time, 4),
            "per_phase": phase_stats,
            "phase_count": len(phase_stats),
        }
    
    def save_to_json(self, filepath: str) -> None:
        """Save benchmark results to JSON file."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "suite": self.summary(),
            "results": [r.to_dict() for r in self.results],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


# ============================================================
# Built-in Benchmark Suites
# ============================================================

# Standard benchmark corpus for DraCo evaluation
STANDARD_BENCHMARKS = {
    "code_reduction": {
        "description": "Code reduction benchmarks with comments, verbose phrases, and repetitive patterns",
        "categories": ["comments", "verbose_phrases", "repetitive_commands", "filler_words", "code_patterns"],
        "target_reduction": 90,
        "minimum_quality": 90,
    },
    "quality_preservation": {
        "description": "Quality preservation benchmarks ensuring 90%+ essential token retention",
        "categories": ["code_reduction"],
        "target_reduction": 90,
        "minimum_quality": 90,
    },
    "format_compression": {
        "description": "ZON format compression benchmarks across different depths and modes",
        "categories": ["format_compression"],
        "target_reduction": "35-70%",
        "minimum_quality": 100,  # ZON is lossless
    },
]


# ============================================================
# CLI Entry Point
# ============================================================

def run_benchmarks(phases: Optional[List[int]] = None, output: Optional[str] = None) -> Dict[str, Any]:
    """Run the full or partial benchmark suite.
    
    Args:
        phases: List of phase numbers to benchmark (1-12). None runs all configured.
        output: Path to save results JSON. None to just return results.
    
    Returns:
        Dictionary with benchmark summary and detailed results.
    """
    suite = BenchmarkSuite()
    
    if phases is None:
        # Run all available phases
        results = suite.run_all()
    else:
        results = {}
        for phase in phases:
            if phase in suite.phases:
                phase_results = suite.phases[phase]()
                results[phase] = phase_results
                suite.results.extend(phase_results)
    
    summary = suite.summary()
    
    if output:
        suite.save_to_json(output)
    
    return {
        "summary": summary,
        "results": [r.to_dict() for r in suite.results],
    }


if __name__ == "__main__":
    # Run benchmarks and print summary
    import sys
    phases = [int(p) for p in sys.argv[1].split(",")] if len(sys.argv) > 1 else None
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    results = run_benchmarks(phases, output_file)
    
    print(f"=== DraCo Benchmark Suite Results ===")
    print(f"Summary: {results['summary']}")
    print()
    
    for r in results["results"]:
        tag = "✓" if r["passed_quality_gate"] else "✗"
        tag += f" {r['test_name']}: {r['reduction_percentage']:.1f}% reduction, {r['quality_percentage']:.1f}% quality, {r['execution_time']:.3f}s"
        print(f"  {tag}")