FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY src/ src/
COPY data/ /data

RUN pip install uv
RUN uv pip install --system -r requirements.txt
RUN pip install -e .

RUN useradd -m appuser && \
    mkdir -p /app/cache /app/.streamlit && \
    chown -R appuser:appuser /app

ENV HF_HOME=/app/cache
ENV STREAMLIT_CONFIG_DIR=/app/.streamlit

USER appuser

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]