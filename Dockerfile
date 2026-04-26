FROM python:3.14-slim

WORKDIR /app

RUN pip install uv \
    && addgroup --system app \
    && adduser --system --ingroup app --home /app app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
COPY alembic.ini ./alembic.ini
COPY migrations/ ./migrations/
COPY main.py gunicorn.conf.py ./
COPY scripts/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh \
    && chown -R app:app /app

ENV PATH="/app/.venv/bin:$PATH" \
    HOME="/app"

USER app

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
