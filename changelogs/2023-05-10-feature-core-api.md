### Added
- [ChronAm JSON API] at /api/chronam/
  - Original endpoints were [changed to JSON-LD IIIF
    responses](https://github.com/open-oni/open-oni/pull/127). Original
    responses are now available again. Read more about Open ONI API resources in
    the [About API markup](/core/templates/about_api.html).
  - Now powered by [Django Rest Framework] which provides throttling, auth, etc
  - Include new error checking and testing
  - Update `/about/api/` text & `<link rel="alternate">` links on relevant pages
  - Throttling of the API by IP can be enabled with the environment variable
    `ONI_CHRONAM_API_THROTTLE`. Read more in [configuration
    documentation](/docs/customization/configuration.md#onisitesettings_basepy)

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

### Contributors
- Greg Tunink (techgique)
