FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

EXPOSE 8000

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "algodaily.wsgi:application"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
