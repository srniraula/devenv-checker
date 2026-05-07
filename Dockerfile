FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"
COPY --from=builder /root/.local /root/.local
COPY devcheck.py .
ENTRYPOINT ["python", "devcheck.py"]
