FROM python:3.13-alpine

WORKDIR /app

COPY src/ .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
