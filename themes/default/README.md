# Default Theme for Open ONI

## Creating your own theme

This theme is included as part of Open ONI to demonstrate how a theme functions. You can use it out of the box, but if you wish to make changes to it you should make a copy of the theme. Your folder structure will end up looking like this:

- ./themes
  - default
  - YOUR_THEME_NAME_HERE

Now add the following to `/settings_local.py`:
```
INSTALLED_APPS = (
    ...

    # Open ONI
    'django.contrib.humanize',  # Added to make data more human-readable
    'sass_processor',
    'themes.YOUR_THEME_NAME_HERE',
    'themes.default',
    'core',
)
```

The INSTALLED_APPS directive will overwrite the default in `django_defaults.py`.

## Customizing your theme

Any file from `/core` you have in your theme will use your file rather than `/core`.

Common files to override will be in `core/templates/` and the `__overrides.html`
file. `__overrides.html` allows you to override or extend blocks of code in
`__base.html` which defines common HTML such as header, navbar, breadcrumbs, and
footer.

### __overrides.html Example:

You don't want to show breadcrumbs in your site. Looking in `__base.html` in `/core`, you can see that the breadcrumbs are contained in a block called breadcrumbs:

```
{% block breadcrumbs %}
```

In `__overrides.html` you can disable breadcrumbs by adding

```
{% block breadcrumbs %}{% endblock breadcrumbs %}
```

which will replace the breadcrumbs block in `__base.html` with nothing.

### Template block extension
To keep what's in the default block in `__base.html` but add to it, include the
`{{ block.super }}` tag in your block, e.g.:

```
{% block head_site_meta %}
  {{ block.super }}

  {# Additional markup #}
{% endblock head_site_meta %}
```

### Bootstrap

If you wanted to overwrite the `boostrap.min.css` file with your own, you could drop it into:

- ./themes
  - YOUR_THEME_NAME_HERE
    - static
      - vendor
        - bootstrap
          - css
            - boostrap.min.css

This may be useful if you want to compile your own `bootstrap.min.css` using sass or less or the online generator.

