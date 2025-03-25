FROM registry.access.redhat.com/ubi9/python-312:9.5 AS base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/
USER root
RUN uv sync --frozen --no-install-project --no-dev
COPY .env src /app
RUN uv sync --frozen --no-dev

FROM base
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8501
CMD ["streamlit", "run", "/app/__init__.py", "--server.port=8501", "--server.address=0.0.0.0"]
