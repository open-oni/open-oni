### Security

### Fixed

### Added
- Restore [ChronAm JSON API] at /api/chronam/

[ChronAm JSON API]: https://chroniclingamerica.loc.gov/about/api/#json-views

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
