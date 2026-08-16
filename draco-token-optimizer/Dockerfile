# DraCo Token Optimizer v2.0.0 - Dockerfile
# Comprehensive token optimization for AI coding agents
# Dual package: pip + npm support

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml requirements*.txt ./

# Install draco package
RUN pip install --no-cache-dir draco-token-optimizer

# Copy application code
COPY draco/ draco/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DRACO_ENVIRONMENT=production
ENV REDUCTION_TARGET=90
ENV QUALITY_THRESHOLD=90

# Expose default MCP port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
  CMD draco health || exit 1

# Default command
ENTRYPOINT ["draco"]

# Default command help
CMD ["--help"]