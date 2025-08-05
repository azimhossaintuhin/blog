FROM python:3.12-slim 
WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pillow 
COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
EXPOSE 8000

CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
