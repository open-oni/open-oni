# Default Theme for Open-Oni

## Creating your own theme

This theme is included as part of Open ONI to demonstrate how a theme functions. You can use it out of the box, but if you wish to make changes to it you should make a copy of the theme and add the following to `/settings_local.py`:

```
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'themes.YOUR_THEME_NAME_HERE',
    'core',
)
```

The INSTALLED_APPS directive will overwrite the directive in `/settings_base.py`.

Your folder structure will end up looking like this:

- ./themes
  - default
  - YOUR_THEME_NAME_HERE

## Overwriting files

Any file from `/core` you have in your theme will use your file rather than `/core`.

### Includes and _overrides.html

Common files to override will be includes (found in `.../template/includes`) and the `__overrides.html` file. Includes contain common html such as header, footer, and navbar. `__overrides.html` allows you to override blocks of code in `__base.html`.

#### Includes example

You want to add icons to the footer of your site. So, you *copy* the `base_footer.html` file from `/core/templates/includes` to your theme `/theme/YOUR_THEME_NAME_HERE/template/includes` and make changes as needed.

#### __override.html Example:

You don't want to show breadcrumbs in your site. Looking in `__base.html` in `/core`, you can see that the breadcrumbs are contained in a block called breadcrumbs:

```{% block breadcrumbs %}```

In `__overrides.html` you can disable breadcrumbs by adding

```{% block breadcrumbs %}{% endblock breadcrumbs %}```

which will replace the breadcrumbs block in `__base.html` with nothing.

### bootstrap

If you wanted to overwrite the `boostrap.min.css` file with your own, you could drop it into:

- ./themes
  - YOUR_THEME_NAME_HERE
    - static
      - vendor
        - bootstrap
          - css
            - boostrap.min.css

This may be useful if you want to compile your own `bootstrap.min.css` using sass or less or the online generator.

