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
        - [Error Emails](#error-emails)
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

#### Error Emails
Django provides the ability to [send emails about 5xx error and 404 responses an
app generates](https://docs.djangoproject.com/en/1.11/howto/error-reporting/).
They can be a bit spammy, but we include documentation about how to enable them
if anyone wants to try them out.

One must add an additional middleware in `settings_local.py`:

```py
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'core.middleware.TooBusyMiddleware',                          # Open ONI
        'django.middleware.http.ConditionalGetMiddleware',            # Open ONI
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.common.BrokenLinkEmailsMiddleware',        # Open ONI
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
```

Additional configuration is required for how and to whom Django sends emails:

```py
    """
    Optional email error reporting
    https://docs.djangoproject.com/en/1.11/howto/error-reporting/

    EMAIL_HOST settings only necessary if another server or service sends email.
    Defaults to 'localhost', sending from the same server running Django.
    Additional settings for further email host configuration:
    https://docs.djangoproject.com/en/1.11/ref/settings/#email-host
    """
    #EMAIL_HOST = 'YOUR_EMAIL_HOST'
    #EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_HOST_PASSWORD'
    #EMAIL_HOST_USER = 'YOUR_EMAIL_HOST_USER'

    """
    'From' address on error emails sent to ADMINS and MANAGERS:
    If sending email from different server, replace `@' + url.netloc` with host.
    """
    #SERVER_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@' + url.netloc

    # ADMINS receive 5xx error emails; MANAGERS receive 404 error emails.
    #ADMINS = [
    #    ('YOUR_admin1', 'YOUR_admin1@example.com'),
    #    ('YOUR_adminX', 'YOUR_adminX@example.com')
    #]
    #MANAGERS = [
    #    ('YOUR_mngr1', 'YOUR_mngr13@example.com'),
    #    ('YOUR_mngrX', 'YOUR_mngrX4@example.com')
    #]
    #IGNORABLE_404_URLS = [
    #    re.compile(r'YOUR_known_404_URL_regex_to_prevent_emails'),
    #]
```

## Compile Static Assets
Run these commands as a regular user rather than root

```bash
cd /opt/openoni
source ENV/bin/activate

# Note: compilescss commands only necessary for production environment
./manage.py compilescss
./manage.py collectstatic -c
./manage.py compilescss --delete-files

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

# For batches to be visible in /batches page, must be released
# Add --reset flag to clear release dates and recalculate them
# Release date and time come from:
# 1. bag-info.txt, if found in the batch source
# 2. Tab-delimited CSV file if provided in format: batch_name \t batch_date
# 3. http://chroniclingamerica.loc.gov/batches.xml
# 4. Current server datetime
./manage.py release

# Run a script with nohup in the background to ingest multiple batches quietly
# nohup prevents scripts from exiting if one closes the terminal shell
nohup (command) >> nohup.out
```

