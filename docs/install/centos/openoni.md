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
    - [Error Emails](#error-emails)
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

### Error Emails
Django provides the ability to [send emails about 5xx error and 404 responses an
app generates](https://docs.djangoproject.com/en/2.2/howto/error-reporting/).
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
    https://docs.djangoproject.com/en/2.2/howto/error-reporting/

    EMAIL_HOST settings only necessary if another server or service sends email.
    Defaults to 'localhost', sending from the same server running Django.
    Additional settings for further email host configuration:
    https://docs.djangoproject.com/en/2.2/ref/settings/#email-host
    """
    #EMAIL_HOST = 'YOUR_EMAIL_HOST'
    #EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_HOST_PASSWORD'
    #EMAIL_HOST_USER = 'YOUR_EMAIL_HOST_USER'

    """
    'From' address on error emails sent to ADMINS and MANAGERS:
    If sending email from different server, replace `@' + url.hostname` with host.
    """
    #SERVER_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@' + url.hostname

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

## Migrate Database
```bash
cd /opt/openoni
source ENV/bin/activate
./manage.py migrate
```
