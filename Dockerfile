FROM python:3.12-slim
WORKDIR /app
COPY devcheck.py .
ENTRYPOINT ["python", "devcheck.py"]
CMD []