FROM mygeodjango:3.11.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "API_2042.wsgi"]