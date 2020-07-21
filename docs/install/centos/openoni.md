# Open ONI Django App

**Contents**

- [Dependencies](#dependencies)
- [Install](#install)
    - [File-based Cache Directory](#file-based-cache-directory)
    - [Python Dependencies](#python-dependencies)
    - [Newspaper Data Symlink](#newspaper-data-symlink)
- [Configure](#configure)
    - [Local Settings](#local-settings)
        - [Theme and Plugins](#theme-and-plugins)
        - [Title and Project Name](#title-and-project-name)
    - [Logging](#logging)
    - [URLs](#urls)
- [Migrate Database](#migrate-database)

## Dependencies
- Download the [Open ONI files](/docs/install/centos/README.md#open-oni-files)
- Prepare the [Python environment](/docs/install/centos/README.md#python-environment)
- Install and configure required [services](/docs/install/centos/services/)

## Install

### File-based Cache Directory
This is used when the app is not running with `DEBUG` enabled. The file path is
defined in `settings_local.py`.

```bash
sudo mkdir -p /var/tmp/django_cache
sudo chown apache /var/tmp/django_cache
sudo chmod 2770 /var/tmp/django_cache
```

### Python Dependencies
Install Open ONI's Python dependencies

```bash
cd /opt/openoni/
source ENV/bin/activate
pip install -r requirements.lock
```

### Newspaper Data Symlink
If you wish to symlink Open ONI's batches directory to another path, e.g.
`/var/local/newspapers`, run these commands

```bash
rm -rf data/batches
ln -s /var/local/newspapers data/batches
```

## Configure

### Local Settings
```bash
cp settings_local_example.py settings_local.py
```

Follow instructions within for the appropriate deployment environment

#### Theme and Plugins
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
    'themes.nebraska',
    'themes.default',
    'core',
)
```

#### Title and Project Name
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

### Logging
Create symlink at `/var/log/openoni` to `/opt/openoni/log`

```bash
ln -s /opt/openoni/log /var/log/openoni
```

### URLs
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

## Migrate Database
```bash
cd /opt/openoni
source ENV/bin/activate
./manage.py migrate
```
