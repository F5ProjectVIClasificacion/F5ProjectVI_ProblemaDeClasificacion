# syntax=docker/dockerfile:1.5
FROM python:3.11-slim

#tells the interpreter not to emit .pyc files during container runs,
#preventing unnecessary filesystem churn on ephemeral storage
ENV PYTHONDONTWRITEBYTECODE=1 \
    # forces Python to flush standard output and error streams immediately
    # rather than buffering them. That behavior keeps container logs aligned
    # with real-time execution, which is important when monitoring or debugging a service running inside Docker
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
#creates a non-root user named appuser inside the image and, with --create-home,
# provisions a home directory for that account. Running the container as this
# unprivileged user later on improves security because application processes no longer inherit root-level permissions.
RUN useradd --create-home appuser

#copies the entire project into the image while assigning ownership to appuser, 
# ensuring the non-root account can read and write the files it needs at runtime.
COPY --chown=appuser:appuser . .

#switches the runtime identity from root to the previously created appuser, so
# every subsequent instruction—and the container’s default process—runs with 
# reduced privileges, hardening the image against escalation attacks
USER appuser

CMD ["python", "src/train_model.py"]
