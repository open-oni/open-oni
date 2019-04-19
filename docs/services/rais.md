# RAIS

**Contents**

- [Install](#install)
    - [Dependencies](#dependencies)
    - [Clone from GitHub](#clone-from-github)
    - [Configure Permissions](#configure-permissions)
    - [Configure Docker Compose](#configure-docker-compose)
        - [Override File](#override-file)
    - [Add Apache Config](#add-apache-config)


## Install

### Dependencies

```bash
yum install docker docker-compose
systemctl enable docker
systemctl start docker
```

### Clone from GitHub

```bash
mkdir /var/local/docker
chmod 750 /var/local/docker
cd /var/local/docker
git clone https://github.com/uoregon-libraries/rais-image-server rais

cd rais

# Switch to master branch
git checkout master
```

### Configure Permissions
```bash
# Set SELinux context on files to be mounted in container
semanage fcontext -a -t container_file_t "/var/local/docker/rais/(?:cap-max|rais-example)\.toml"
restorecon -F -R /var/local/docker/rais

semanage fcontext -a -t container_file_t "/opt/openoni/data/batches(/.*)?"
restorecon -F -R /opt/openoni/data/batches

# Set file permissions for newspaper files
cd /opt/openoni/data/batches
chmod -R g+rwX (batch_name or * for all)
chmod -R o+rX (batch_name or * for all)
find . -type d -exec chmod g+s {} \;
find . -type f -exec chmod -x {} \;
```

### Configure Docker Compose
Define custom docker-compose config file

`vim docker-compose.override.yml`:
```yml
version: "3.4"

services:
  rais:
    image: uolibraries/rais
    environment:
      - RAIS_ADDRESS
      - RAIS_LOGLEVEL
      - RAIS_TILEPATH
      - RAIS_IIIFURL
      - RAIS_INFOCACHELEN
      - RAIS_TILECACHELEN
      - RAIS_IMAGEMAXAREA
      - RAIS_IMAGEMAXWIDTH
      - RAIS_IMAGEMAXHEIGHT
      - RAIS_PLUGINS
    volumes:
      - /opt/openoni/data/batches:/var/local/images:ro
      - ./rais-example.toml:/etc/rais.toml:ro
      - ./cap-max.toml:/etc/rais-capabilities.toml:ro
    ports:
      - 12415:12415
    restart: always
```

Define environment file for docker-compose use which overrides defaults
from `rais-example.toml` mounted as `/etc/rais.toml`. Default values from this
config file are commented for reference.

`vim .env`:
```bash
#RAIS_ADDRESS=:12415
RAIS_LOGLEVEL=INFO
#RAIS_TILEPATH=/var/local/images
RAIS_IIIFURL=https://domain.tld/rais
#RAIS_INFOCACHELEN=10000
#RAIS_TILECACHELEN=0
#RAIS_IMAGEMAXAREA=104857600
#RAIS_IMAGEMAXWIDTH=20480
#RAIS_IMAGEMAXHEIGHT=20480
# Must match at least one plugin,
# but without other ENV var datadog plugin stays disabled
RAIS_PLUGINS=datadog.so
```

Start RAIS docker container

`docker-compose -f docker-compose.override.yml up -d`

#### Override File
Docker Compose is supposed to automatically use a `docker-compose.override.yml`
file if present, but the CentOS 7 version does not appear to do this, thus still
using the `-f  docker-compose.override.yml` option above.

To simplify using Docker Compose commands, we recommend creating a local-only
git branch where the override file is moved to `docker-compose.yml` and the
extra option can be omitted

### Add Apache Config
Copy [RAIS Apache config](/conf/apache/rais.conf) into the drop-in directory which will be included in your virtual host block

```bash
cp /opt/openoni/conf/apache/rais.conf /etc/httpd/local/vhosts/_vhost-includes/
```

