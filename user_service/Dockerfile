FROM python:3.10

WORKDIR /app

COPY . /app

# Copy the global_salt.txt file into the container
COPY global_salt.txt /app/global_salt.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "user_service.py"]
