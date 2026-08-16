# DraCo Token Optimizer - ML Metrics Module
"""Machine learning metrics and evaluation for token optimization.

Provides comprehensive metrics tracking, quality assessment, and performance
measurement for all DraCo optimization operations including reduction ratios,
quality preservation, and agent compatibility metrics.
"""

import time
import json
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from draco.config import (
    REDUCTION_TARGET,
    QUALITY_THRESHOLD,
    MINIMUM_QUALITY_PRESERVATION,
    MAXIMUM_TOKEN_REDUCTION,
    QUALITY_GATES_ENFORCED,
    NUM_QUALITY_GATES,
    REPORT_FORMAT,
    REPORT_TYPES,
)


# ============================================================
# Metrics Result Data Classes
# ============================================================

@dataclass
class MetricsResult:
    """Metrics result from a token optimization operation."""
    operation_id: str
    reduction_percentage: float
    quality_percentage: float
    passed_quality_gate: bool
    verdict: str
    execution_time_ms: float
    timestamp: float
    metadata: Optional[Dict] = None


@dataclass
class QualityMetrics:
    """Quality metrics for token optimization."""
    original_tokens: int
    reduced_tokens: int
    remaining_tokens: int
    quality_score: float  # 0.0 to 1.0 (will be converted to percentage)
    quality_threshold: float
    reduction_achieved: float  # Percentage
    below_threshold: bool
    gate_details: Dict[str, bool]


@dataclass
class ReductionMetrics:
    """Reduction metrics across multiple operations."""
    total_original: int
    total_reduced: int
    total_remaining: int
    average_reduction_percentage: float
    average_quality_percentage: float
    minimum_quality: float
    maximum_quality: float
    std_dev_quality: float
    gate_pass_rate: float
    all_met_target: bool


# ============================================================
# Core Metrics Functions
# ============================================================

def calculate_reduction_metrics(
    original_tokens: int,
    reduced_tokens: int,
    quality_score: float,
    quality_threshold: float = None,
) -> QualityMetrics:
    """Calculate quality metrics for a reduction operation.
    
    Args:
        original_tokens: Number of tokens before reduction
        reduced_tokens: Number of tokens after reduction
        quality_score: Quality score (0.0 to 1.0)
        quality_threshold: Minimum quality threshold (uses config default if None)
        
    Returns:
        QualityMetrics with detailed analysis
    """
    if quality_threshold is None:
        quality_threshold = get_quality_threshold() / 100.0
    
    # Calculate percentages
    reduction_percentage = ((original_tokens - reduced_tokens) / original_tokens * 100) if original_tokens > 0 else 0.0
    quality_percentage = quality_score * 100.0
    remaining_percentage = (reduced_tokens / original_tokens * 100) if original_tokens > 0 else 100.0
    
    # Check if below threshold
    below_threshold = quality_percentage < (quality_threshold * 100)
    
    # Gate details - simplified check list
    gate_details = {
        "reduction_target_met": reduction_percentage >= REDUCTION_TARGET,
        "quality_above_threshold": quality_percentage >= (quality_threshold * 100),
        "essential_content_preserved": reduced_tokens > 0,
        "verdict_appropriate": quality_percentage >= 50,  # Basic sanity check
        "no_negative_tokens": reduced_tokens >= 0,
        "quality_score_valid": 0.0 <= quality_score <= 1.0,
    }
    
    # Count passed gates
    passed_gates = sum(1 for v in gate_details.values() if v)
    total_gates = len(gate_details)
    
    return QualityMetrics(
        original_tokens=original_tokens,
        reduced_tokens=reduced_tokens,
        remaining_tokens=reduced_tokens,
        quality_score=quality_score,
        quality_threshold=quality_threshold,
        reduction_achieved=reduction_percentage,
        below_threshold=below_threshold,
        gate_details=gate_details,
    )


def calculate_reduction_metrics_batch(
    results: List[MetricsResult],
) -> ReductionMetrics:
    """Calculate aggregate reduction metrics across multiple operations.
    
    Args:
        results: List of MetricsResult objects
        
    Returns:
        ReductionMetrics with aggregate statistics
    """
    if not results:
        return ReductionMetrics(
            total_original=0,
            total_reduced=0,
            total_remaining=0,
            average_reduction_percentage=0.0,
            average_quality_percentage=0.0,
            minimum_quality=1.0,
            maximum_quality=0.0,
            std_dev_quality=0.0,
            gate_pass_rate=0.0,
            all_met_target=False,
        )
    
    # Aggregate token counts
    total_original = sum(r.metadata.get('original_tokens', 0) if r.metadata else 0 for r in results)
    total_reduced = sum(r.metadata.get('reduced_tokens', 0) if r.metadata else 0 for r in results)
    total_remaining = total_reduced  # Same meaning
    
    # Calculate average reduction percentage
    reduction_percentages = [r.reduction_percentage for r in results if r.reduction_percentage is not None]
    average_reduction = sum(reduction_percentages) / len(reduction_percentages) if reduction_percentages else 0.0
    
    # Calculate average quality percentage
    quality_percentages = [r.quality_percentage for r in results if r.quality_percentage is not None]
    average_quality = sum(quality_percentages) / len(quality_percentages) if quality_percentages else 0.0
    
    # Quality stats
    quality_scores = [r.quality_percentage for r in results if r.quality_percentage is not None]
    minimum_quality = min(quality_scores) if quality_scores else 1.0
    maximum_quality = max(quality_scores) if quality_scores else 0.0
    
    # Standard deviation of quality
    if len(quality_scores) > 1:
        import statistics
        std_dev_quality = statistics.stdev(quality_scores)
    else:
        std_dev_quality = 0.0
    
    # Gate pass rate
    passed_gates = sum(1 for r in results if r.passed_quality_gate)
    gate_pass_rate = round(passed_gates / len(results) * 100, 2) if results else 0.0
    
    # Check if all met the reduction target
    all_met_target = all(r.reduction_percentage >= REDUCTION_TARGET for r in results if r.original_tokens > 0)
    
    return ReductionMetrics(
        total_original=total_original,
        total_reduced=total_reduced,
        total_remaining=total_remaining,
        average_reduction_percentage=round(average_reduction, 2),
        average_quality_percentage=round(average_quality, 2),
        minimum_quality=round(minimum_quality, 2),
        maximum_quality=round(maximum_quality, 2),
        std_dev_quality=round(std_dev_quality, 2),
        gate_pass_rate=gate_pass_rate,
        all_met_target=all_met_target,
    )


# ============================================================
# Metrics Tracking
# ============================================================

class MetricsTracker:
    """Tracks metrics across DraCo operations for continuous improvement."""
    
    def __init__(self):
        self.operation_history: List[MetricsResult] = []
        self.reduction_history: List[QualityMetrics] = []
        self.quality_history: List[float] = []  # Quality scores over time
        self.reduction_history_list: List[float] = []  # Reduction percentages over time
        self.start_time = time.time()
        self.total_operations = 0
        self.total_reductions = 0
        self.total_tokens_processed = 0
        self.total_tokens_reduced = 0
    
    def record_operation(self, result: MetricsResult):
        """Record a metrics result from an operation."""
        self.operation_history.append(result)
        self.total_operations += 1
        
        if result.metadata:
            orig = result.metadata.get('original_tokens', 0)
            red = result.metadata.get('reduced_tokens', 0)
            if orig > 0:
                self.total_tokens_processed += orig
                self.total_tokens_reduced += red
    
    def record_quality_metrics(self, metrics: QualityMetrics):
        """Record quality metrics for trend analysis."""
        self.reduction_history.append(metrics)
        self.quality_history.append(metrics.quality_score)
    
    def record_reduction_percentage(self, percentage: float):
        """Record a reduction percentage for trend analysis."""
        self.reduction_history_list.append(percentage)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all tracked metrics."""
        operations = len(self.operation_history)
        
        # Calculate overall statistics
        if self.quality_history:
            avg_quality = sum(self.quality_history) / len(self.quality_history)
            min_quality = min(self.quality_history)
            max_quality = max(self.quality_history)
        else:
            avg_quality = 0.0
            min_quality = 1.0
            max_quality = 0.0
        
        if self.reduction_history_list:
            avg_reduction = sum(self.reduction_history_list) / len(self.reduction_history_list)
            min_reduction = min(self.reduction_history_list)
            max_reduction = max(self.reduction_history_list)
        else:
            avg_reduction = 0.0
            min_reduction = 100.0
            max_reduction = 0.0
        
        # Gate pass rate from last 100 operations
        recent_ops = self.operation_history[-100:] if len(self.operation_history) > 100 else self.operation_history
        recent_passed = sum(1 for r in recent_ops if r.passed_quality_gate)
        recent_pass_rate = round(recent_passed / len(recent_ops) * 100, 2) if recent_ops else 0.0
        
        # Trend analysis (compare first half vs second half)
        quality_trend = "stable"
        reduction_trend = "stable"
        
        if len(self.quality_history) >= 20:
            mid = len(self.quality_history) // 2
            first_half_avg = sum(self.quality_history[:mid]) / mid
            second_half_avg = sum(self.quality_history[mid:]) / (len(self.quality_history) - mid)
            
            if second_half_avg > first_half_avg * 1.05:
                quality_trend = "improving"
            elif second_half_avg < first_half_avg * 0.95:
                quality_trend = "degrading"
        
        if len(self.reduction_history_list) >= 20:
            mid = len(self.reduction_history_list) // 2
            first_half_avg = sum(self.reduction_history_list[:mid]) / mid
            second_half_avg = sum(self.reduction_history_list[mid:]) / (len(self.reduction_history_list) - mid)
            
            if second_half_avg > first_half_avg * 1.05:
                reduction_trend = "increasing"
            elif second_half_avg < first_half_avg * 0.95:
                reduction_trend = "decreasing"
        
        return {
            "total_operations": operations,
            "total_tokens_processed": self.total_tokens_processed,
            "total_tokens_reduced": self.total_tokens_reduced,
            "overall_average_quality": round(avg_quality, 2),
            "overall_quality_minimum": round(min_quality, 2),
            "overall_quality_maximum": round(max_quality, 2),
            "overall_average_reduction": round(avg_reduction, 2),
            "overall_reduction_minimum": round(min_reduction, 2),
            "overall_reduction_maximum": round(max_reduction, 2),
            "recent_pass_rate": recent_pass_rate,
            "quality_trend": quality_trend,
            "reduction_trend": reduction_trend,
            "continuous_learning_enabled": CONTINUOUS_LEARNING,
        }
    
    def check_degradation(self, threshold: float = 0.85) -> Dict[str, Any]:
        """Check for quality degradation over time.
        
        Args:
            threshold: Quality threshold for degradation detection (0.0-1.0)
            
        Returns:
            Degradation analysis report
        """
        if len(self.quality_history) < 50:
            return {
                "degradation_detected": False,
                "message": "Insufficient data for degradation analysis (need at least 50 operations)",
                "current_quality": self.quality_history[-1] if self.quality_history else None,
            }
        
        # Compare recent 25 operations vs earlier 25
        recent = self.quality_history[-25:]
        earlier = self.quality_history[-50:-25] if len(self.quality_history) >= 50 else self.quality_history[:25]
        
        recent_avg = sum(recent) / len(recent)
        earlier_avg = sum(earlier) / len(earlier)
        
        degradation_ratio = recent_avg / earlier_avg if earlier_avg > 0 else 1.0
        
        degradation_detected = degradation_ratio < threshold
        
        return {
            "degradation_detected": degradation_detected,
            "current_average_quality": round(recent_avg, 4),
            "previous_average_quality": round(earlier_avg, 4),
            "degradation_ratio": round(degradation_ratio, 4),
            "threshold": threshold,
            "recent_quality_trend": "declining" if degradation_detected else "stable_or_improving",
            "action_required": "trigger_self_healing" if degradation_detected else "none",
        }


# ============================================================
# Quality Gate Functions
# ============================================================

def run_quality_gates(
    quality_metrics: QualityMetrics,
    custom_gates: Dict[str, bool] = None,
) -> Dict[str, Any]:
    """Run quality gate checks on reduction metrics.
    
    Args:
        quality_metrics: QualityMetrics from a reduction operation
        custom_gates: Optional custom gate checks
        
    Returns:
        Gate results dictionary
    """
    # Default quality gates (based on config)
    default_gates = {
        "reduction_target_90_percent": quality_metrics.reduction_achieved >= 90,
        "quality_above_90_percent": quality_metrics.quality_score * 100 >= 90,
        "essential_content_preserved": quality_metrics.reduced_tokens > 0,
        "no_quality_collapse": quality_metrics.quality_score >= 0.3,  # Minimum 30% quality
        "verdict_appropriate": quality_metrics.quality_score * 100 >= 50,
        "tokens_positive": quality_metrics.reduced_tokens >= 0,
        "quality_score_valid": 0.0 <= quality_metrics.quality_score <= 1.0,
    }
    
    # Merge with custom gates if provided
    all_gates = {**default_gates, **(custom_gates or {})}
    
    # Count passed/failed
    passed = sum(1 for v in all_gates.values() if v)
    total = len(all_gates)
    pass_rate = round(passed / total * 100, 2) if total > 0 else 0.0
    
    # Determine if overall quality gate passes
    overall_pass = pass_rate >= 90  # 90% of gates must pass (matching quality threshold)
    
    # Add gate-specific details
    gate_details = {}
    for gate_name, gate_passed in all_gates.items():
        gate_details[gate_name] = {
            "passed": gate_passed,
            "metric_value": _get_gate_metric_value(gate_name, quality_metrics),
            "threshold": _get_gate_threshold(gate_name),
        }
    
    return {
        "overall_pass": overall_pass,
        "pass_rate": pass_rate,
        "total_gates": total,
        "passed_gates": passed,
        "failed_gates": total - passed,
        "gate_details": gate_details,
        "quality_metrics": quality_metrics,
        "recommendation": _get_quality_gate_recommendation(all_gates, quality_metrics),
    }


def _get_gate_metric_value(gate_name: str, metrics: QualityMetrics) -> Any:
    """Get the metric value relevant to a specific gate."""
    values = {
        "reduction_target_90_percent": metrics.reduction_achieved,
        "quality_above_90_percent": metrics.quality_score * 100,
        "essential_content_preserved": metrics.reduced_tokens,
        "no_quality_collapse": metrics.quality_score,
        "verdict_appropriate": metrics.quality_score * 100,
        "tokens_positive": metrics.reduced_tokens,
        "quality_score_valid": metrics.quality_score,
    }
    return values.get(gate_name, None)


def _get_gate_threshold(gate_name: str) -> float:
    """Get the threshold for a specific gate."""
    thresholds = {
        "reduction_target_90_percent": 90,
        "quality_above_90_percent": 90,
        "essential_content_preserved": 1,  # Just check > 0
        "no_quality_collapse": 0.3,
        "verdict_appropriate": 50,
        "tokens_positive": 0,
        "quality_score_valid": 1.0,
    }
    return thresholds.get(gate_name, 0.0)


def _get_quality_gate_recommendation(
    all_gates: Dict[str, bool],
    metrics: QualityMetrics,
) -> str:
    """Get recommendation based on quality gate results."""
    failed = [name for name, passed in all_gates.items() if not passed]
    
    if not failed:
        return "continue_optimization - all gates passed"
    
    # Categorize failures
    critical_failures = [f for f in failed if "quality" in f.lower() or "reduction" in f.lower()]
    non_critical_failures = [f for f in failed if f not in critical_failures]
    
    if critical_failures:
        if "quality_above_90_percent" in critical_failures:
            return f"reduce_reduction_target - quality at {round(metrics.quality_score * 100, 1)}% below 90% threshold"
        elif "reduction_target_90_percent" in critical_failures:
            return f"increase_reduction - current reduction at {round(metrics.reduction_achieved, 1)}% below 90% target"
        else:
            return f"adjust_both - {', '.join(critical_failures)} need attention"
    
    if non_critical_failures:
        return f"minor_adjustments - {', '.join(non_critical_failures)} need minor tuning"
    
    return "continue_optimization"


# ============================================================
# Export Functions
# ============================================================

__all__ = [
    "MetricsResult",
    "QualityMetrics",
    "ReductionMetrics",
    "calculate_reduction_metrics",
    "calculate_reduction_metrics_batch",
    "MetricsTracker",
    "run_quality_gates",
    "_get_gate_metric_value",
    "_get_gate_threshold",
    "_get_quality_gate_recommendation",
]