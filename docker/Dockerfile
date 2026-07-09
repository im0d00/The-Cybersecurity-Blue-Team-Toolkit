FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY rules ./rules
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "blueteam_toolkit.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
