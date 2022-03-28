### Changed
- Switch ONI Docker image base to Ubuntu Focal LTS for Python 3.8
  - Change pip-install.sh to install wheel package to prevent bdist_wheel errors
- Docker Compose
  - Switch to use the latest Solr 8.x release
  - Switch to MariaDB 10.6 LTS release
    - Update config to specify `utf8mb3` charset and collation to prevent
      charset collation mismatch error when `utf8(mb3)` charset oddly defaults
      to collation `utf8mb4_general_ci`
    - Remove unused config file variables
- Update OpenSeadragon to 2.4.2
- Update tablesorter to 2.31.3
- Update Dependency Roadmap
- Rename `requirements.pip` to `requirements.txt`
- Update Django to 3.2
  - https://docs.djangoproject.com/en/3.2/releases/3.2/
  - https://docs.djangoproject.com/en/3.2/internals/deprecation/
    - Update `urls.py`, example files, and documentation to no longer use
      deprecated `django.conf.urls`

### Removed
- Deprecated `default_app_config` line in `core/__init__.py`

### Migration
- If upgrading to MariaDB 10.6.1+, be aware of `utf8` character set default
  changes: https://mariadb.com/kb/en/mariadb-1061-release-notes/#character-sets
  - See documentation for compatible character sets and collations:
    https://mariadb.com/kb/en/supported-character-sets-and-collations/
  - Also see Django recommendations:
    https://docs.djangoproject.com/en/3.2/ref/databases/#creating-your-database
    - TL;DR use `utf8_general_ci` rather than `utf8_unicode_ci` unless you
      require German multi-character comparison to match German DIN-1 ordering
- If you use any deployment scripts or CI/CD that interact with
  `requirements.pip`, note that this file has been renamed to `requirements.txt`
  to function with GitHub's dependency graph security scanning
- Django 3.2 changes
  - Update theme template tags from `{% load static from staticfiles %}` to
    `{% load static %}` if not already done. This was deprecated in Django 2.2
    and is now removed.
  - Update any path building in settings files using `BASE_DIR`, `LOG_LOCATION`,
    `STATIC_ROOT`, and `STORAGE` to use Path syntax, e.g.
    `BASE_DIR / 'subdir1' / 'subdir2'`
    - Code working with these paths outside settings files like
      `os.path.join(settings.LOG_LOCATION, 'subdir')` must be updated by adding
      import line `from pathlib import Path` and changing code to
      `Path(settings.LOG_LOCATION) / 'subdir'`; `import os` may then be removed
      - Other corresponding code changes:
        https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module
  - Update `urls.py` files to use
    `from django.urls import include, path, re_path` rather than
    `from django.conf.urls import url, include`. Then search and replace `url(`
    to `re_path(`, though non-regex patterns should use just `path(`
  - Remove `default_app_config` lines in all apps' `__init__.py` files

### Contributors
- techgique
