FROM ghcr.io/praekeltfoundation/docker-django-bootstrap-nw:py3.10-buster

COPY . /app
WORKDIR /app
RUN pip install -e .

# temporary until there is a new PyCap Release
ENV DJANGO_SETTINGS_MODULE "latestnumbers.settings.production"
CMD [\
    "latestnumbers.wsgi:application",\
    "--workers=2",\
    "--threads=4",\
    "--worker-class=gthread",\
    "--worker-tmp-dir=/dev/shm"\
]