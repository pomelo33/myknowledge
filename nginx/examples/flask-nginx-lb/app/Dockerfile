FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask redis
CMD ["python","app.py"]
#CMD ["python","app_redis.py"]