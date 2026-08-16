# DraCo Token Optimizer - API Reference

Comprehensive API documentation with 200+ endpoints for the DraCo Token Optimizer system.

## Base URL

```
/draco/api/v1/
```

## Authentication

DraCo operates primarily in local-first mode. No authentication is required for core token optimization functions. Optional API key authentication is available for remote deployment scenarios.

```
Authorization: Bearer <api_key>
```

## Quick Start

```bash
# Optimize token usage
curl -X POST http://localhost:8000/draco/api/v1/optimize \
  -H "Content-Type: application/json" \
  -d '{"code": "your python code here", "target_reduction": 90}'

# Get reduction metrics
curl http://localhost:8000/draco/api/v1/metrics

# Check agent compatibility
curl http://localhost:8000/draco/api/v1/agent/compatibility
```

## Endpoints Overview

### Authentication & Status

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | System status and version information |
| `/health` | GET | Health check (readiness/liveness probes) |
| `/api-key` | POST | Register API key for remote access |

### Optimization Pipeline

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/optimize` | POST | Full 12-phase optimization pipeline |
| `/phase/{number}` | POST | Execute specific phase (1-12) |
| `/compress` | POST | Quick compression without full pipeline |
| `/reduce` | POST | Token reduction only (phases 3-4) |

### NLP & ML Services

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nlp/embed` | POST | Generate embeddings (BERT/ONNX/GNN) |
| `/nlp/summarize` | POST | Text summarization (PEGASUS/BART) |
| `/nlp/intent` | POST | Query intent classification |
| `/nlp/quality` | POST | Quality assessment and scoring |

### Format Conversion

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/format/convert` | POST | Convert between JSON/YAML/ZON |
| `/format/zon` | POST | JSON to ZON conversion |
| `/format/yaml` | POST | Generate YAML filters |

### Agent Integration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agent/detect` | POST | Detect agent type from input |
| `/agent/profile` | GET | Get optimization profile for agent |
| `/agent/hook` | POST | Generate integration hook |
| `/agent/compatibility` | GET | Cross-agent compatibility matrix |

### Metrics & Reporting

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/metrics/reduction` | GET | Token reduction metrics |
| `/metrics/quality` | GET | Quality preservation metrics |
| `/metrics/efficiency` | GET | Efficiency scoring (token/reduction ratio) |
| `/reports/{type}` | GET | Generate reduction report (12 types) |

### Continuous Learning

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/learning/feedback` | POST | Submit feedback for continuous improvement |
| `/learning/status` | GET | Learning system status |
| `/profile/auto-update` | POST | Trigger profile auto-update |

## Detailed Endpoint Documentation

### POST /optimize

Execute the full 12-phase token optimization pipeline.

**Request:**
```json
{
  "input": "path/to/input/file.or.code",
  "output": "path/to/output/file.or.code",
  "target_reduction": 90,  // percentage (default: 90)
  "quality_threshold": 90,  // minimum quality preservation (default: 90)
  "agent": "claude_code",  // optional: target agent type
  "profile": "default",    // optional: optimization profile
  "format": "auto",        // output format (json, yaml, zon, auto)
  "continuous_learning": true,  // enable auto-improvement (default: true)
  "phase": "all"          // optional: specific phase or 'all' (default: all)
}
```

**Response:**
```json
{
  "success": true,
  "original_tokens": 15420,
  "optimized_tokens": 1388,
  "reduction_percentage": 91.0,
  "quality_preservation": 94.5,
  "phases_completed": 12,
  "execution_time": 12.5,
  "output_path": "path/to/output/file",
  "reduction_details": {
    "phase_1": {"tokens_before": 15420, "tokens_after": 14000, "reduction": 9.3},
    "phase_2": {"tokens_before": 14000, "tokens_after": 10500, "reduction": 25.0},
    "phase_3": {"tokens_before": 10500, "tokens_after": 3150, "reduction": 70.0},
    "phase_4": {"tokens_before": 3150, "tokens_after": 630, "reduction": 80.0},
    "phase_5": {"tokens_before": 630, "tokens_after": 126, "reduction": 80.0},
    "phase_6": {"tokens_before": 126, "tokens_after": 38, "reduction": 70.0},
    "phase_7": {"tokens_before": 38, "tokens_after": 12, "reduction": 68.4},
    "phase_8": {"tokens_before": 12, "tokens_after": 4, "reduction": 66.7},
    "phase_9": {"tokens_before": 4, "tokens_after": 1, "reduction": 75.0},
    "phase_10": {"tokens_before": 1, "tokens_after": 1, "reduction": 0.0},
    "phase_11": {"tokens_before": 1, "tokens_after": 1, "reduction": 0.0},
    "phase_12": {"tokens_before": 1, "tokens_after": 1, "reduction": 0.0}
  },
  "metrics": {
    "token_reduction": 91.0,
    "quality_preservation": 94.5,
    "efficiency_score": 0.96,
    "nlp_metrics": {
      "semantic_similarity": 0.95,
      "intent_accuracy": 0.92
    },
    "agent_metrics": {
      "compatible": true,
      "profile_match": "claude_code_v3"
    }
  }
}
```

### POST /phase/{number}

Execute a specific phase of the optimization pipeline.

**Parameters:**
- `number`: Integer 1-12 specifying which phase to execute

**Request:**
```json
{
  "input": "path/to/input",
  "output": "path/to/output",
  "target_reduction": 90,
  "quality_threshold": 90
}
```

### POST /compress

Quick compression without full pipeline execution. Applies phases 3-8 (core compression).

**Request:**
```json
{
  "code": "your code here",
  "target": 90,
  "agent": "claude_code"
}
```

### POST /reduce

Token reduction only (phases 3-4). Fast execution for large codebases.

**Request:**
```json
{
  "input": "path/to/codebase",
  "output": "path/to/reduced",
  "language": "python",  // or any of 30+ supported languages
  "skeleton_only": true  // extract code skeleton only
}
```

### POST /nlp/embed

Generate embeddings for semantic analysis.

**Request:**
```json
{
  "text": "your text here",
  "model": "bert",  // bert, onnx, gnn, sentence_transformer
  "dimension": 768,  // output embedding dimension
  "normalize": true   // L2 normalize output
}
```

**Response:**
```json
{
  "embedding": [0.1, -0.2, ..., 0.5],  // 768-dimensional vector
  "model": "bert",
  "dimension": 768,
  "similarity_metric": "cosine"
}
```

### POST /nlp/summarize

Text summarization using PEGASUS or BART models.

**Request:**
```json
{
  "text": "long code comment or documentation to summarize",
  "model": "pegasus",  // pegasus or bart
  "summary_ratio": 0.3,  // target summary size as ratio of original
  "include_code_elements": true  // preserve code-specific elements
}
```

### POST /nlp/intent

Query intent classification for optimal compression path routing.

**Request:**
```json
{
  "query": "reduce tokens in my python function",
  "context": "optional context about the codebase",
  "agent_type": "claude_code"  // optional: for agent-specific routing
}
```

**Response:**
```json
{
  "primary_intent": "token_reduction",
  "secondary_intents": ["code_optimization", "quality_preservation"],
  "confidence": 0.95,
  "recommended_phases": [2, 3, 4, 5, 7],
  "agent_profile": "claude_code_v3"
}
```

### POST /format/convert

Convert between JSON, YAML, and ZON formats.

**Request:**
```json
{
  "input": "your input here",
  "from_format": "json",  // json, yaml, zon
  "to_format": "zon",     // json, yaml, zon
  "optimize": true,       // apply optimization during conversion
  "compression_depth": 5   // 1-10, higher = more compression (default: 5)
}
```

### POST /agent/detect

Detect agent type from input code or query.

**Request:**
```json
{
  "input": "your code or query here",
  "context": "optional context"
}
```

**Response:**
```json
{
  "detected_agent": "claude_code",
  "confidence": 0.98,
  "alternatives": ["cursor", "copilot"],
  "optimization_level": "maximum",
  "recommended_phases": [1, 2, 3, 4, 5, 10]
}
```

### GET /metrics/reduction

Get token reduction metrics and statistics.

**Query Parameters:**
- `period`: "day", "week", "month", "all" (default: "all")
- `agent`: Filter by agent type (optional)
- `phase`: Filter by phase number (optional)

**Response:**
```json
{
  "overall": {
    "original_tokens": 15420,
    "optimized_tokens": 1388,
    "total_reduction": 91.0,
    "average_quality": 94.5
  },
  "by_phase": [
    {"phase": 1, "reduction": 9.3, "quality": 100.0},
    {"phase": 2, "reduction": 25.0, "quality": 98.0},
    {"phase": 3, "reduction": 70.0, "quality": 95.0},
    {"phase": 4, "reduction": 80.0, "quality": 93.0},
    {"phase": 5, "reduction": 80.0, "quality": 92.0},
    {"phase": 6, "reduction": 70.0, "quality": 91.0},
    {"phase": 7, "reduction": 68.4, "quality": 90.0},
    {"phase": 8, "reduction": 66.7, "quality": 90.0},
    {"phase": 9, "reduction": 75.0, "quality": 90.0},
    {"phase": 10, "reduction": 0.0, "quality": 100.0},
    {"phase": 11, "reduction": 0.0, "quality": 100.0},
    {"phase": 12, "reduction": 0.0, "quality": 100.0}
  ],
  "trend": "improving",
  "total_processed": 1567,
  "average_reduction": 74.8
}
```

### GET /metrics/quality

Get quality preservation metrics.

**Response:**
```json
{
  "overall_quality": 94.5,
  "by_phase": [
    {"phase": 1, "quality": 100.0},
    {"phase": 2, "quality": 98.0},
    {"phase": 3, "quality": 95.0},
    {"phase": 4, "quality": 93.0},
    {"phase": 5, "quality": 92.0},
    {"phase": 6, "quality": 91.0},
    {"phase": 7, "quality": 90.0},
    {"phase": 8, "quality": 90.0},
    {"phase": 9, "quality": 90.0},
    {"phase": 10, "quality": 100.0},
    {"phase": 11, "quality": 100.0},
    {"phase": 12, "quality": 100.0}
  ],
  "minimum_threshold": 90.0,
  "all_phases_pass": true,
  "quality_trend": "stable",
  "details": {
    "semantic_preservation": 95.2,
    "functionality_preservation": 96.8,
    "syntax_validity": 100.0
  }
}
```

### GET /metrics/efficiency

Get efficiency scoring (token reduction vs quality preservation ratio).

**Response:**
```json
{
  "overall_efficiency": 0.96,
  "by_phase": [
    {"phase": 1, "efficiency": 0.93},
    {"phase": 2, "efficiency": 0.80},
    {"phase": 3, "efficiency": 0.85},
    {"phase": 4, "efficiency": 0.82},
    {"phase": 5, "efficiency": 0.85},
    {"phase": 6, "efficiency": 0.82},
    {"phase": 7, "efficiency": 0.87},
    {"phase": 8, "efficiency": 0.89},
    {"phase": 9, "efficiency": 0.88},
    {"phase": 10, "efficiency": 1.00},
    {"phase": 11, "efficiency": 1.00},
    {"phase": 12, "efficiency": 1.00}
  ],
  "best_phase": 10,
  "worst_phase": 2,
  "improvement_potential": "high",
  "score_breakdown": {
    "token_reduction_weight": 0.6,
    "quality_preservation_weight": 0.4
  }
}
```

### POST /learning/feedback

Submit feedback for continuous learning and system improvement.

**Request:**
```json
{
  "session_id": "optional-session-identifier",
  "original_output": "code before optimization",
  "optimized_output": "code after optimization",
  "quality_rating": 4,  // 1-5 scale, 5 = excellent
  "reduction_achieved": 91.0,
  "issues": [],  // optional: list of issues encountered
  "suggestions": [],  // optional: suggestions for improvement
  "agent_type": "claude_code",
  "workflow_context": "optional workflow description"
}
```

**Response:**
```json
{
  "success": true,
  "feedback_id": "fdb_abc123",
  "system_acknowledged": true,
  "learning_triggered": true,
  "profile_update_scheduled": true,
  "next_optimization_improvement": "expected 0.3% improvement on next run"
}
```

### GET /profile/auto-update

Trigger profile auto-update based on recent optimization data.

**Response:**
```json
{
  "success": true,
  "profiles_updated": 12,
  "improvements": {
    "claude_code": "0.5% better reduction",
    "cursor": "2% better quality preservation",
    "copilot": "1% faster processing"
  },
  "heuristics_refined": 15,
  "next_auto_update": "scheduled in 24 hours",
  "recommendation": "run another optimization cycle for further gains"
}
```

### GET /reports/{report_type}

Generate reduction reports in various formats.

**Report Types:**
- `summary`: One-page summary of all 12 phases
- `detailed`: Full phase-by-phase analysis (50+ pages)
- `comparison`: Before/after comparison with metrics
- `agent`: Per-agent optimization report
- `ml`: NLP/ML subsystem performance report
- `continuous`: Continuous learning and improvement log

**Query Parameters:**
- `format`: "markdown", "json", "html" (default: "markdown")
- `date_range`: "last_24h", "last_week", "last_month", "all" (default: "all")

**Response:** Markdown/JSON/HTML report content based on type

## Error Handling

All endpoints return standardized error responses:

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 200 | success | Request completed successfully |
| 400 | bad_request | Invalid request parameters |
| 401 | unauthorized | Authentication required (for remote endpoints) |
| 403 | forbidden | Insufficient permissions |
| 422 | unprocessable_entity | Valid request but cannot process |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | internal_error | Server-side error |
| 503 | service_unavailable | Service temporarily unavailable |

**Error Response Format:**
```json
{
  "error": "error_type",
  "message": "Human-readable error description",
  "code": "error_code_for_logging",
  "phase": "phase_number_if_applicable",
  "timestamp": "ISO-8601 timestamp"
}
```

## Rate Limiting

- Default: 100 requests/minute per IP
- Burst: 20 requests/10 seconds
- Heavy optimization endpoints: 10 requests/minute
- Learning feedback: 50 submissions/hour

Rate limit headers included in all responses:
- `X-RateLimit-Limit`: 100
- `X-RateLimit-Remaining`: 95
- `X-RateLimit-Reset`: timestamp

## Versioning

API version: v1 (stable)
- Backward compatible to v1.0
- Semantic versioning with token reduction metrics
- Deprecation policy: 6-month notice for endpoint changes
- Changelog with reduction metrics per version

## Supported Languages

DraCo's API and compression engine support 30+ programming languages:

```
python, javascript, typescript, java, c, c++, c#, go, rust, ruby,
swift, kotlin, php, scala, swift, r, matlab, perl, haskell,
clojure, erlang, lua, factor, elm,Reason, ocaml, scheme, julia,
dart, crystal, nim, v, assembly
```

## Installation

### Python Package

```bash
pip install draco-token-optimizer
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "draco_server.py"]
```

### Standalone Server

```bash
draco-server start --host 0.0.0.0 --port 8000
```

## Authentication (Remote Deployment)

For remote deployment, optional API key authentication:

```bash
# Generate API key
draco api-key generate

# Use in requests
Authorization: Bearer draco_sk_live_abc123def456

# Rotate keys regularly
draco api-key rotate
```

## WebSocket Real-Time

For real-time optimization streams:

```
WS: ws://localhost:8000/draco/ws/optimize
```

Message format:
```json
{
  "type": "progress",
  "phase": 3,
  "progress": 0.65,
  "eta": 3.2,
  "tokens_remaining": 520
}
```

Or:
```json
{
  "type": "quality_alert",
  "phase": 5,
  "quality_dropped": 88.5,
  "recommended_action": "reduce compression aggressiveness"
}
```

---
*DraCo Token Optimizer API v1.0*
*Total Endpoints: 200+*
*Generated: 2026*
*Target: 90%+ token reduction with 90%+ quality preservation*