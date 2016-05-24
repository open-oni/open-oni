FROM ubuntu:trusty
MAINTAINER Mark Cooper <mark.cooper@lyrasis.org>

ENV DJANGO_SETTINGS_MODULE openoni.settings

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
  apache2 \
  ca-certificates \
  gcc \
  git \
  graphicsmagick \
  libapache2-mod-wsgi \
  libmysqlclient-dev \
  libxml2-dev \
  libxslt-dev \
  libjpeg-dev \
  mysql-client \
  python-dev \
  python-virtualenv \
  supervisor

RUN a2enmod cache expires rewrite
ADD apache/openoni.conf /etc/apache2/sites-available/openoni.conf
RUN a2dissite 000-default.conf
RUN a2ensite openoni

RUN git clone https://github.com/open-oni/open-oni.git /opt/openoni

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
WORKDIR /opt/openoni
RUN mkdir -p data/batches && mkdir -p data/cache && mkdir -p data/bib
RUN virtualenv ENV && \
  source /opt/openoni/ENV/bin/activate && \
  cp conf/openoni.pth ENV/lib/python2.7/site-packages/openoni.pth && \
  pip install -U distribute && \
  pip install -r requirements.pip --allow-all-external
ADD settings.py /opt/openoni/settings.py

RUN install -d /opt/openoni/static && install -d /opt/openoni/.python-eggs

ADD load_batch.sh /load_batch.sh
ADD startup.sh /startup.sh
ADD test.sh /test.sh

RUN chmod u+x /load_batch.sh && chmod u+x /startup.sh && chmod u+x /test.sh

EXPOSE 80
CMD ["/startup.sh"]
