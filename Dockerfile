FROM ghcr.io/praekeltfoundation/docker-django-bootstrap-nw:py3.10-buster

COPY ./requirements.txt /app/
COPY ./setup.py /app/

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app
# temporary until there is a new PyCap Release
ENV DJANGO_SETTINGS_MODULE "latestnumbers.settings.production"
CMD [\
    "latestnumbers.wsgi:application",\
    "--workers=2",\
    "--threads=4",\
    "--worker-class=gthread",\
    "--worker-tmp-dir=/dev/shm"\
]