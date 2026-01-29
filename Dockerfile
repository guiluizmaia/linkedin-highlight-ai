FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (ffmpeg for video processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

# Create tmp directory for database
RUN mkdir -p tmp

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "agent.py"]
