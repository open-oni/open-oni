### Security

### Fixed

### Added
- [ChronAm JSON API] at /api/chronam/`
  - Now powered by [Django Rest Framework]
  - Includes new error checking and testing
  - Update `/about/api/` text and `<link rel="alternate">` links on relevant pages

[ChronAm JSON API]: https://chroniclingamerica.loc.gov/about/api/#json-views
[Django Rest Framework]: https://www.django-rest-framework.org/

### Changed

### Removed

### Migration
- Add previously omitted Django apps `auth` and `contenttpes`
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

### Deprecated

### Contributors
- Greg Tunink (techgique)
