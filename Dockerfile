## BASE STAGE ##
FROM python:3.11-slim as base

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Ignore 'Running pip as the root user...' warning
ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip

## BUILDER STAGE ##
FROM base as builder

# Install Poetry
RUN pip install poetry==1.8.3

# Copy project files
COPY ["pyproject.toml", "poetry.lock", "README.md", "./"]
COPY ["src/", "src/"]

# Build wheel
RUN poetry build --format wheel

## PRODUCTION STAGE ##
FROM base as production

# Copy and install the application wheel
COPY --from=builder /app/dist/*.whl /app/

# Update package list, install required packages, clean up, create user and group,
# create directories, set permissions
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    addgroup --system app && adduser --system --ingroup app app

# Install app wheel and gunicorn
RUN pip install --no-cache-dir gunicorn /app/*.whl

# Expose the application port
EXPOSE 8080

COPY ["main.py", "gunicorn.conf.py", "./"]

# Change to the non-root user
RUN usermod -u 10001 app || useradd -u 10001 -m app
USER app

# Command to run the application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "main:app"]