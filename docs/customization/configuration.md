# Configuring Your App

## `settings_local.py`

Unlike a vanilla django installation, our `onisite/settings.py` is not where
all settings are stored. This file actually combines django's defaults
(`onisite/django_defaults.py`), the Open ONI defaults
(`onisite/settings_base.py`), and your local configuration
(`onisite/settings_local.py`).

Basic site customizations can be done by creating `onisite/settings_local.py`
in the same location you find `onisite/settings_base.py`, and overriding
values. The easiest option is to copy the example file:

```bash
cp onisite/settings_local_example.py onisite/settings_local.py
```

Then adjust settings, particularly those starting with `YOUR`.

There are many settings in the example file which are based on environment
variables and/or other settings. Only change these if you understand the
ramifications of doing so. Most users will be fine just letting those stay
as-is.

That said, overrides are simple - you just redefine a value. For example, you
could do a simple change to enable TIFFs by putting this line into your
`onisite/settings_local.py`:

```python
USE_TIFF = True
```

Or you could do something more complex like adding an app to override the
default theme:

```python
# Add "mytheme" app before core so it takes precedence
INSTALLED_APPS = (
  'django.contrib.humanize',
  'django.contrib.staticfiles',

  'themes.mytheme',
  'themes.default',
  'core',
)
```

Additional settings are documented in [`onisite/settings_base.py`](https://github.com/open-oni/open-oni/blob/master/onisite/settings_base.py).
Most simple installations will not need to override these settings, but they
are available for advanced users.

## onisite/urls.py

Copy the example file:

```bash
cp onisite/urls_example.py onisite/urls.py
```

For most setups, that's all you need to do!

If you add an app or theme that's more than just UI changes, it's possible
you'll have to add its routing rules to `onisite/urls.py`. A simple example
might be adding a state map app which has handlers for displaying itself.

Let's say you're running an ONI site at `http://example.com`. If you add
something like this to your file, you'd be telling the `statemap` app to handle
anything under `http://example.com/map`:

```python
  url('^map/', include("statemap.urls")),
```

## Environment Configuration

If you start with the supplied `settings_local_example.py` for your site, you
will have a variety of environment-specified settings, allowing you to
customize the site using simple environment variables. If you're using
docker-compose, you can also opt to configure these values via a
`docker-compose.override.yml` or an `.env` file. (You can copy `.env.example`
to `.env` and alter `.env` as necessary)

The environment-driven settings are meant to be the ones most likely to need to
be altered across different environments, such as development vs. staging vs.
production.

The current list of settings you'll need to understand (as of v0.11), and an
explanation, follows:

- `HTTPPORT` (default = `80`): The website's HTTP port exposed on the host
 machine
- `ONI_BASE_URL` (default = `http://localhost`): This must be the URL which
 reaches the ONI site. For development this is usually kept at the default.
 For production, it could be something like `https://oregonnews.uoregon.edu`.
 If your HTTPPORT isn't the default (80 for `http`, 443 for `https`), you need
 to include that here, e.g., `http://demo.example.org:8080`)
- `ONI_DEBUG` (default = `1`): If set to 1, the site is put in debug mode,
 which should **never** be used for a live site. Various development-friendly
 setttings are configured from this.
- `ONI_LOG_SQL` (default = `0`): If set to 1, more logs than you ever wanted
 will be printed out. Useful for debugging what ONI is doing with the
 database.
- `ONI_LOG_TO_FILE` (default = `0`): If set to 1, logs are printed to a file in
 your ONI root's `log` subdirectory.
- `ONI_SECRET_KEY` (default = `openoni`): Used by Django for form security. In
 ONI this is currently of minimal importance since we have no web-based
 authentication or administration commands. However, it's good practice to
 set this to a highly random string in case that changes in the future.
- `RDBMSPORT` (default = `3306`): The port which is exposed to the docker host
 for accessing MariaDB locally.
- `SOLRPORT` (default = `8983`): The port which is exposed to the docker host
 for accessing Solr locally. In production you do *not* want this set to
 anything exposed to the outside world!

Some settings exist which you generally shouldn't need to change for a default
docker-compose setup, but should still understand:

- `APACHE_LOG_LEVEL` (default = `warn`): Log level for Apache. Values lower
 than `warn` tend to produce a lot of chatter.
- `ONI_DB_HOST` (default = `rdbms`): Hostname for the MariaDB server. If using
 docker-compose, this *and all other database settings* should remain
 unchanged unless you know what you're doing!
- `ONI_DB_PORT` (default = `3306`): Database port, almost always 3306.
- `ONI_DB_NAME` (default = `openoni`): Database name.
- `ONI_DB_USER` (default = `openoni`): Database username.
- `ONI_DB_PASSWORD` (default = `openoni`): Database user's password.
- `ONI_SOLR_URL` (default = `http://solr:8983/solr/openoni`)
- `ONI_STORAGE_PATH` (default = `/var/local/openoni-data`)
