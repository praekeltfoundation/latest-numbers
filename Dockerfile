FROM python:3.10.6-slim-buster

COPY ./requirements.txt /app/
COPY ./setup.py /app/

RUN pip install -r /app/requirements.txt

COPY . /app

# temporary until there is a new PyCap Release
ENV DJANGO_SETTINGS_MODULE "latestnumbers.settings.production"
RUN SECRET_KEY=placeholder ALLOWED_HOSTS=placeholder python manage.py collectstatic --noinput
CMD [\
    "latestnumbers.wsgi:application",\
    "--workers=2",\
    "--threads=4",\
    "--worker-class=gthread",\
    "--worker-tmp-dir=/dev/shm"\
]