FROM docker.io/python:3.12-slim AS base

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get -y install --no-install-recommends \
  gcc \
  libmariadb-dev \
  libxml2-dev \
  libxslt-dev \
  libjpeg-dev \
  pkg-config

# Set up initial directory and Python environment before copying the rest of
# the app in
WORKDIR /opt/openoni
COPY requirements.lock .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.lock
RUN pip install gunicorn

# I *think* this is necessary to get the initial volumes populated for themes
# and plugins
VOLUME /opt/openoni/themes
VOLUME /opt/openoni/onisite/plugins

# Now copy the rest of the app - nothing below here should be expensive or
# fetch external dependencies
COPY . .

# Config is copied into here and symlinked back into onisite in order to
# provide a nice config-only mount option
VOLUME /var/local/oni-config

# Settings that we want set in all environments, and which should never (or
# very rarely) be changed in a container setup
ENV ONI_STORAGE_PATH=/var/local/oni-data/
ENV ONI_DB_HOST=rdbms
ENV ONI_DB_PORT=3306
ENV ONI_DB_NAME=openoni
ENV ONI_DB_USER=openoni
ENV ONI_SOLR_URL=http://solr:8983

# It should be obvious but we want it to be very clear that ONI's data path
# *must* be a volume, not ephemeral
VOLUME /var/local/oni-data

ENTRYPOINT ["/entrypoint.sh"]

FROM base AS app

# gunicorn defaults - the config file has these as well, but this makes it
# clearer what we've made configurable via environment
ENV GUNICORN_WORKERS=4
ENV GUNICORN_MAX_REQUESTS=10000

# Get gunicorn config file in place: this makes ENV vars work
COPY docker/python/gunicorn.conf.py /etc/gunicorn.conf.py

COPY docker/python/entrypoint.sh /entrypoint.sh
CMD ["gunicorn", "-c", "/etc/gunicorn.conf.py"]

FROM app AS test

# Test just needs custom settings and the stripped-down test entrypoint
COPY onisite/test_settings.py /opt/openoni/onisite/settings_local.py
COPY onisite/urls_example.py /opt/openoni/onisite/urls.py
COPY docker/python/test-entrypoint.sh /entrypoint.sh
CMD ["/opt/openoni/manage.py", "test", "--settings=onisite.test_settings"]
