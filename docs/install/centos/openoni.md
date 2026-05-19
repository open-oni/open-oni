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
defined in the `CACHES` dictionary in `settings_base.py`, but may be overridden
in `settings_local.py`.

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

This will install the versions of Python dependencies last tested by Open ONI
maintainers, but it is likely that dependencies such as Django have released
newer versions. We do not plan to make Open ONI releases based on dependency
releases outside of severe security vulnerabilities or breaking changes. We may
mention dependency releases such as Django updates in the #general channel of
our Slack workspace.

We encourage you to review `requirements.txt` which [controls the versions pip
may install](https://pip.pypa.io/en/stable/user_guide/#requirements-files) and
make a plan to update your dependencies and test regularly for security
maintenance.

Update Python dependencies based on `requirements.txt`:

```bash
cd /opt/openoni/
source ENV/bin/activate
pip install -U -r requirements.txt

# Update requirements.lock for repeatable installs
pip freeze > requirements.lock
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
cp onisite/settings_local_example.py onisite/settings_local.py
```

Follow instructions within for the appropriate deployment environment

#### Theme and Plugins
Add your theme and plugin customizations to `INSTALLED_APPS`:

```py
# List of configuration classes / app packages in order of priority high to low.
# The first item in the list has final say when collisions occur.
INSTALLED_APPS = (
    # Default
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Humanize and local theme override all below
    'django.contrib.humanize',  # Makes data more human-readable

    # Plugins
    # See https://github.com/open-oni?q=plugin for available plugins

    # Open ONI
    # Extend the default theme by including your own above themes.default
    # 'themes.YOUR_THEME_NAME',
    'themes.default',
    'core',
)
```

#### Title and Project Name
Set the title and project name text for the website

```py
SITE_TITLE = "YOUR_SHORT_PROJECT_NAME"
PROJECT_NAME = "YOUR_LONG_PROJECT_NAME"
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

Edit `onisite/urls.py` as needed for plugins and themes following instructions
within the file.

## Migrate Database
```bash
cd /opt/openoni
source ENV/bin/activate
./manage.py migrate
```
