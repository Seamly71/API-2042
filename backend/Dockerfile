FROM seamly71/mygeodjango:3.11.9
# Зачем я залил зависимости в dockerhub читайте в mygeodjango/readme.txt

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "API_2042.wsgi"]