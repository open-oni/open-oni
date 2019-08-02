# Open ONI

**Contents**

- [Dependencies](#dependencies)
- [Install](#install)
    - [Clone Open ONI](#clone-openoni)
    - [SELinux Permissions](#selinux-permissions)
    - [File-based Cache Directory](#file-based-cache-directory)
    - [Python Virtual Environment](#python-virtual-environment)
    - [Migrate Database](#migrate-database)
    - [Newspaper Data Symlink](#newspaper-data-symlink)
- [Configure](#configure)
    - [Solr Schema](#solr-schema)
    - [Django](#django)
        - [Local Settings](#local-settings)
            - [Theme and Plugins](#theme-and-plugins)
            - [Title and Project Name](#title-and-project-name)
        - [Logging](#logging)
        - [URLs](#urls)
        - [WSGI Path](#wsgi-path)
- [Compile Static Assets](#compile-static-assets)
- [Load Batches](#load-batches)


## Dependencies
Install [required services](/docs/services/)

`yum install python-virtualenv`


## Install

### Clone Open ONI

```bash
chgrp webadmins /opt
chmod 2775 /opt
cd /opt
```

Run these commands as a regular user rather than root
```
git clone git@github.com:open-oni/open-oni.git openoni
cd openoni

# Check out the desired branch or release, e.g.:
git checkout dev
```

### SELinux Permissions
```bash
# Python executables need httpd-executable SELinux context
semanage fcontext -a -t httpd_sys_script_exec_t "/opt/openoni/ENV/lib/python2.7/site-packages/.+\.so"

# Static asset path needs Apache write access
mkdir /opt/openoni/static/compiled
semanage fcontext -a -t httpd_sys_rw_content_t "/opt/openoni/static/compiled(/.*)?"

restorecon -F -R /opt/openoni/
```

### File-based Cache Directory
This is only used if the production settings file is enabled in Open ONI's `settings_local.py`

```bash
mkdir -p /var/tmp/django_cache
chown apache /var/tmp/django_cache
chmod 2770 /var/tmp/django_cache
```

### Python Virtual Environment
Run these commands as a regular user rather than root

```bash
cd /opt/openoni

# Create and activate Python virtual environment
virtualenv ENV
source ENV/bin/activate

# Update pip and setuptools
pip install -U pip
pip install -U setuptools

# Install / update Open ONI dependencies
pip install -U -r requirements.pip
```

### Migrate Database
Run these commands as a regular user rather than root

```bash
cd /opt/openoni
source ENV/bin/activate
./manage.py migrate
```

### Newspaper Data Symlink
Run these commands as a regular user rather than root

```bash
cd /opt/openoni
source ENV/bin/activate

rm -rf data/batches
ln -s /var/local/newspapers data/batches

./manage.py batches
```


## Configure

### Solr Schema
```bash
cp /opt/openoni/docker/solr/schema.xml /var/solr/data/openoni/conf/schema.xml
cp /opt/openoni/docker/solr/solrconfig.xml /var/solr/data/openoni/conf/solrconfig.xml
chown -R solr.solr /var/solr/data/openoni

service solr restart
```

### Django

#### Local Settings
```bash
cp settings_local_example.py settings_local.py
```

Follow instructions within for the appropriate deployment environment

##### Theme and Plugins
Add the theme and plugins it incorporates to `INSTALLED_APPS`:

```py
# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
    # Default
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Plugins
    # See https://github.com/open-oni?q=plugin for available plugins
    'onisite.plugins.calendar',
    'onisite.plugins.featured_content',
    'onisite.plugins.map',

    # Open ONI
    'django.contrib.humanize',  # Added to make data more human-readable
    'sass_processor',
    'themes.nebraska',
    'themes.default',
    'core',
)
```

##### Title and Project Name
Set the title and project name text for the website

```py
# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
# for introduction / about / further information / etc
SITE_TITLE = "Nebraska Newspapers"
PROJECT_NAME = "Nebraska Newspapers"
```


#### Logging
Create symlink at `/var/log/openoni` to `/opt/openoni/log`

```bash
ln -s /opt/openoni/log /var/log/openoni
```

#### URLs
Set the URLs file to use the theme and plugins it incorporates

```bash
cp onisite/urls_example.py onisite/urls.py
```

`vim onisite/urls.py`:
```python
# Copy this to urls.py.  Most sites can leave this as-is.  If you have custom
# apps which need routing, modify this file to include those urlconfs.
from django.conf.urls import url, include

# Django documentation recommends always using raw string syntax: r''
urlpatterns = [
  # Plugin URLs
  #url(r'^map/', include("onisite.plugins.map.urls")),

  # Theme URLs
  #url(r'', include("themes.(theme_name).urls")),

  # Open ONI URLs
  url(r'', include("core.urls")),
]
```


## Compile Static Assets
Run these commands as a regular user rather than root

```bash
cd /opt/openoni
source ENV/bin/activate

./manage.py collectstatic -c

# Grant write access for both Apache and group
sudo chown -R apache static/compiled/
sudo chmod -R g+w static/compiled/
```

In production environments, perform a graceful Apache restart after re-compiling static assets so the app uses the updated static file hash fingerprints in the URLs rendered in templates:

```bash
sudo apachectl graceful
```

## Load Batches
Run these commands as a regular user rather than root

```bash
# Repeat as necessary
./manage.py load_batch /opt/openoni/data/batches/(batch_name)/

# Run a script with nohup in the background to ingest multiple batches quietly
# nohup prevents scripts from exiting if one closes the terminal shell
nohup (command) >> nohup.out
```

