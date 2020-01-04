FROM python:3.7-slim
RUN python -m pip install --upgrade pip
RUN python -m pip install grpcio
RUN python -m pip install grpcio-tools
WORKDIR /app
EXPOSE 5000
CMD ["python", "Server.py"]