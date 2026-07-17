### Added
- [ChronAm JSON API] at /api/chronam/
  - Original endpoints were [changed to JSON-LD IIIF
    responses](https://github.com/open-oni/open-oni/pull/127). Original
    responses are now available again.
  - Now powered by [Django REST Framework] which provides throttling, auth, etc
  - Added new error checking and testing, new `count` and `pages` keys
    in `batches.json` responses to aid parsing pagination, and root
    `/api/chronam/` description response with links to resource list URLs
  - Updated `/about/api/` markup and `<link rel="alternate">` links
    on relevant pages
    - Read more about Open ONI API resources in the [About API
      markup](/core/templates/about_api.html).

[ChronAm JSON API]: https://chroniclingamerica.loc.gov/about/api/#json-views
[Django Rest Framework]: https://www.django-rest-framework.org/

### Migration
- Add previously omitted Django apps `auth` and `contenttypes`
  required by Django Rest Framework
  to top of `INSTALLED_APPS` in `onisite/settings_local.py`

```python
INSTALLED_APPS = (
    # Default
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
```

- Throttling of the ChronAm JSON API by IP can be enabled with the environment
  variable `ONI_CHRONAM_API_THROTTLE`. Default to no throttling when env var
  not present. Accepts `#/day`, `#/hour`, `#/minute`, or `#/second` values.
  Read more in [configuration
  documentation](/docs/customization/configuration.md#onisitesettings_basepy)
  - Update `web` service's `environment:` list in `docker-compose.yml` and your
    `.env` file for Docker

### Contributors
- Greg Tunink (techgique)
