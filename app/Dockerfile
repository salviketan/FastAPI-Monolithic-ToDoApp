# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.10.8
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


WORKDIR /backend

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
--disabled-password \
--gecos "" \
--home "/nonexistent" \
--shell "/sbin/nologin" \
--no-create-home \
--uid "${UID}" \
appuser

RUN apt-get update \
&& apt-get -y install libpq-dev gcc && apt-get -y install vim curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN exit
RUN apt-get update
    
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY pyproject.toml uv.lock .python-version .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the source code into the container.
COPY . .

# Final sync to install the app itself
RUN uv sync --frozen --no-dev

# Make non-privileged user owner of app directory
RUN chown -R appuser:appuser ../backend

# Switch to the non-privileged user to run the application.
USER appuser

# Set the virtualenv at the front of the PATH
ENV PATH="/backend/.venv/bin:$PATH"