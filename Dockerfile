FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Copy repo
COPY . /app

# Install dependencies (pyproject.toml / poetry-style)
RUN pip install --upgrade pip && \
    pip install -e .

EXPOSE 8080

CMD ["python", "app.py"]
