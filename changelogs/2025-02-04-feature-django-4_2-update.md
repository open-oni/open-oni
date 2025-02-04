Changelog format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

Please respect the 80-character text margin and follow the [GitHub Flavored
Markdown Spec](https://github.github.com/gfm/).

### Security
- Updates Django to latest available 4.2.x.
- Updates sqlparse to the latest available version.

### Changed
- Fixes for features removed in Django 4.0:
    - Replaces a reference (and removes an unused reference) to
      `django.utils.http.urlquote`, an alias that was removed in Django 4.
      [See original deprecation notice here](
          https://docs.djangoproject.com/en/3.0/releases/3.0/#id3
        ).
    - Replaces `{% ifequal %}` and `{% ifnotequal %}` tags with their
      `{% if %}` equivalents.
    - Changes the docker/django-admin script to call django-admin instead
      of django-admin.py, which was removed in 4.0.
- Changes settings to adopt the following Django 4.2 defaults:
  - Removes `SECURE_BROWSER_XSS_FILTER` (
       https://docs.djangoproject.com/en/4.0/releases/4.0/#securitymiddleware-no-longer-sets-the-x-xss-protection-header
     )
  - Removes now-redundant `USE_L10N = True` (
        https://docs.djangoproject.com/en/4.0/releases/4.0/#use-l10n-deprecation
      )
  - "To allow serving a Django site on a subpath without changing the value of
    STATIC_URL, the leading slash is removed from that setting (now 'static/')
    in the default startproject template."
    (https://docs.djangoproject.com/en/4.0/releases/4.0/#miscellaneous)
  - The STATICFILES_STORAGE setting is deprecated in favor of
    STORAGES["staticfiles"].
    (https://docs.djangoproject.com/en/4.2/releases/4.2/#id1)
- Replaces usages of the deprecated `Logger.warn()` with `Logger.warning()`
  (A Python thing, not a Django 4 thing.)

### Removed
- See all features removed in Django
  [4.0](https://docs.djangoproject.com/en/4.2/releases/4.0/#features-removed-in-4-0),
  [4.1](https://docs.djangoproject.com/en/4.2/releases/4.1/#features-removed-in-4-1).
- Notable removals include:
  - `{% ifequal %}` and `{% ifnotequal %}` template tags.
  - Various django.utils helper functions and aliases. 

### Migration
- Check themes and plugins for code that is not compatible with Django 4.x:
  - Look for usages of `{% ifequal %}` and `{% ifnotequal %}` in theme
    and plugin templates and replace them with `{% if %}` tags
    and the `==` or `!=` operators.
  - Review Django 4.x release notes with special attention to
    [features removed in 4.0](
        https://docs.djangoproject.com/en/5.1/releases/4.0/#features-removed-in-4-0
      ) and [features removed in 4.1](
        https://docs.djangoproject.com/en/5.1/releases/4.1/#features-removed-in-4-1
      ).
- Merge changes from requirements.lock into any project-specific requirements.lock.

### Deprecated
- See features deprecated in Django
  [4.0](https://docs.djangoproject.com/en/4.2/releases/4.0/#features-deprecated-in-4-0),
  [4.1](https://docs.djangoproject.com/en/4.2/releases/4.1/#features-deprecated-in-4-1),
  [4.2](https://docs.djangoproject.com/en/4.2/releases/4.2/#features-deprecated-in-4-2).
- Notable deprecations include:
  - Direct use of time zone APIs from `pytz`
    (https://docs.djangoproject.com/en/4.2/releases/4.0/#zoneinfo-default-timezone-implementation).
  - `STATICFILES_STORAGE` and `DEFAULT_FILE_STORAGE` settings.
    (Not to be confused with `STATIC_ROOT`.)

### Contributors
- Joshua Wier (walkerwier)
