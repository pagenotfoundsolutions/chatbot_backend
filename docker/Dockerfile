FROM python:3.14-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Set the virtual environment path outside of /app
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
# # Install dependencies into the virtual environment
# RUN uv sync --frozen --no-cache
# Install dependencies into the virtual environment (with cache mount for speed)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Copy the application code
COPY . .

# Ensure all directories under app/ have an __init__.py to prevent ModuleNotFoundError
RUN find app -type d -exec touch {}/__init__.py \;

# Ensure the virtual environment's binaries are in the PATH
ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
