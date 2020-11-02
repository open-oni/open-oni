# Configuring Your App

Below details all of the information regarding configuring and customizing your instance of Open ONI.
By default the docker compose version of Open ONI works without any needed overrides or configuration changes.
You should read it carefully and fully understand what and why you are making the changes.
Failure to do so will cause problems. 

- [settings_local.py](#onisitesettings_localpy)
- [Environment Variables](#environment-variables)
- [docker-compose.yml](#docker-composeyml)
- [onisite/settings_base.py](#onisitesettings_basepy)
- [onisite/settings_local.py](#onisitesettings_localpy-1)
- [onisite/urls.py](#onisiteurlspy)

## `onisite/settings_local.py`

Unlike a vanilla Django installation, our `onisite/settings.py` is not where
all settings are stored. This file actually imports Django's defaults
(`onisite/django_defaults.py`), the Open ONI general configuration
(`onisite/settings_base.py`), and your local configuration
(`onisite/settings_local.py`).

First, copy the local settings example file to the filename used:

```bash
cp onisite/settings_local_example.py onisite/settings_local.py
```

For initial customization, search and update values beginning with `YOUR_`.

We recommend remaining configuration be set via [environment
variables](#environment-variables), but additional settings documented in
[`onisite/settings_base.py`](/onisite/settings_base.py) are available for
complex deployments. Keep in mind that additional settings file customizations
could make future Open ONI release upgrades more difficult.

## Environment Variables
These settings are most likely to need to be altered across different
environments, such as development vs. staging vs. production. Environment
variables are used in a few different files and are provided to reduce the need
to customize settings files directly.

### `docker-compose.yml`
Note many settings such as database credentials and URLs shouldn't be changed
for the default docker-compose setup.

If you're using docker-compose, you can also opt to configure these
values via a `docker-compose.override.yml` or `.env` file. You can copy
`.env.example` to `.env` and alter `.env` as necessary.

- `APACHE_LOG_LEVEL` (default = `warn`): Log level for Apache - values beyond
 `warn` tend to produce a lot of extraneous log entries.
- `HTTPPORT` (default = `80`): The website's HTTP port exposed on the host
 machine.

### `onisite/settings_base.py`
- `ONI_DB_HOST` (default = `rdbms`): Hostname for the MariaDB server. If using
 docker-compose, this *and all other database settings* should remain
 unchanged unless you know what you're doing!
- `ONI_DB_PORT` (default = `3306`): Database port, almost always 3306.
- `ONI_DB_NAME` (default = `openoni`): Database name.
- `ONI_DB_USER` (default = `openoni`): Database username.
- `ONI_DB_PASSWORD` (default = `openoni`): Database user's password.
- `ONI_DEBUG` (default = `1`): If set to 1, the site is put in debug mode,
 which should **never** be used for a live site. Various development-friendly
 setttings are enabled based on this.
- `ONI_LOG_LEVEL` (default = `INFO`): Sets [Django's logging
 level](https://docs.djangoproject.com/en/2.2/topics/logging/#loggers). `INFO`
 as the default leans toward logging more information
- `ONI_LOG_SQL` (default = `0`): If set to 1, more logs than you ever wanted
 will be printed out. Useful for debugging what ONI is doing with the
 database.
- `ONI_LOG_TO_FILE` (default = `0`): If set to 1, logs are printed to a file in
 your ONI root's `log` subdirectory.
- `ONI_SECRET_KEY` (default = `openoni`): Used by Django for form security. In
 ONI this is currently of minimal importance since we have no web-based
 authentication or administration commands. However, it's good practice to
 set this to a highly random string in case that changes in the future.
- `ONI_SOLR_URL` (default = `http://solr:8983`): Solr server base URL
- `ONI_STORAGE_PATH` (default = `(ONI base dir path)/data`): Path to batch storage

### `onisite/settings_local.py`
- `ONI_BASE_URL` (default = `http://localhost`): This must be the URL which
 reaches the ONI site. For development this is usually kept at the default.
 For production, it could be something like `https://oregonnews.uoregon.edu`.
 If your docker compose HTTPPORT isn't the default `80` for http, you need to
 include that here, e.g. `http://demo.example.org:8080`.
- `ONI_HSTS_SECONDS` (default = `0`): Enable HSTS cookies for HTTPS security if
 greater than `0`. Suggest testing with a low value like `300` and a higher
 value like `31536000` for long-term use in production
- `ONI_IIIF_URL` (default = BASE_URL + `/images/iiif`): URL at which ONI
 will serve IIIF images, proxied to the IIIF server by Apache

## `onisite/urls.py`

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