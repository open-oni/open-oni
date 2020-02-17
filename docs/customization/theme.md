# Theming

Unless if you are happy with the out-of-the-box Open ONI look, you will probably want a theme!  Open ONI ships with a default theme (`/themes/default`) that you may want to refer to while you work on your own.

Quick reference to update static files (CSS, images, etc) after making changes in the docker dev environment:

```
docker-compose exec web manage collectstatic --noinput
```

Collected static files are stored in the `/static/compiled/` directory. You
will need to compile static assets after making changes to CSS and JS.

- [Create a New Theme](#create-a-new-theme)
- [Customize Your Theme](#customize-your-theme)
- [Common Overrides](#common-overrides)
- [CSS Customization](#css-customization)
- [Compile Static Assets](#compile-static-assets)

View the [plugin documentation](/docs/customization/plugins.md) for more
information about available plugins and information about how to include them
in your application.

## Create a New Theme

You will want to copy the default theme to start your own!

```
cp -r themes/default themes/<your-theme-name>
```

You may base your theme on top of the existing default theme by including them both, or you may prefer just to start entirely from scratch.  Open `onisite/settings_local.py` and paste in the following, changing `your-theme-name` and removing `themes.default` if you do not wish to build your theme on top of it.

```
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'themes.your-theme-name',
    'themes.default',
    'core',
)
```

Go ahead and edit `themes/<your-theme-name>/templates/home.html` and the changes should show up when you restart your app!

## Customize Your Theme

There are a number of ways to customize your theme, from images to CSS to content.  Let's talk a little about templates, first.

Django is set up with templates like `home.html`.  They are chained together so that one template might have the header and footer information, and then next template down will fill content in between the header and footer.  This makes it easier to only change one part of the application when you need to update your footer, rather than having to edit every file in Open ONI.  You can view all the templates and sub-templates at `core/templates`.

Sometimes, you need to override an entire sub-template.  For example, your About page's content is probably not going to be like anybody else's, so it makes sense to copy `core/templates/about.html` into your own theme at `themes/<your-theme-name>/templates/about.html` and change the text.

Most of the time, though, you only need to change little things about the
existing templates.  That's what the `__overrides.html` file is for! This file
sits between `__base.html` and `__l_(layout).html` files, so that you can
override parts of `__base.html` easily.

Let's walk through an example.  Let's say you want to change your footer.  You found the existing footer in `core/templates/__base.html` but you should **never edit core** so you need to override it.  Fortunately, the footer is surrounded by a "block."

```python
{% block footer %}
    <div id="footer">
        <div class="container">
          <p>{{site_title}}</p>
          <p>Site created using <a href="https://github.com/open-oni/open-oni">open-oni</a> software, built off the Library of Congress's <a href="https://github.com/LibraryofCongress/chronam">chronam</a>.</p>
        </div>
    </div>
{% endblock footer %}
```

That block "footer" code is very convenient, because it means that we can define our own block in the overrides and we don't have to change anything in core, nor copy the entire `__base.html` file into our theme!

Open up `themes/<your-theme-name>/templates/__overrides.html`.  Now you can copy in the `{% block footer %} {% endblock footer %}` code and put anything you like in it.

```python
{% block footer %}
  Put your own HTML code in here!!!
{% endblock footer %}
```

Let's say that you want to add some JavaScript to a page.  Here's where things get a little different.  You probably don't want to override the JS that is already operating on each page, so your first instinct might be to copy the existing block and add your code at the bottom.  But wait!  There's a neat method that will help you!  You can use `{{ block.super }}` to tell the app "use all the original code plus my new code!!"  Here's how it looks.

**The original javascript block in __base.html**

```python
{% block javascript %}
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script type="text/javascript" async="" src="{% static 'js/highlight.js' %}"></script>
    <script type="text/javascript" async="" src="{% static 'vendor/bootstrap/js/bootstrap.min.js' %}"></script>
{% endblock javascript %}
```

**Your override for the javascript block in __overrides.html**

```python
{% block javascript %}
    {{ block.super }}
    <script>    // your code here!    </script>
{% endblock javascript %}
```

## Common Overrides

As described above, you can override blocks to use your own HTML.  These blocks may vary by page, for example, `/search/pages/results` has many more blocks than `/about`, so you may need to consult the `core/templates` file to learn more about overriding specific parts.  However, the overall structure of the base template has the following blocks which may be overridden in `themes/<your-theme-name>/templates/__overrides.html`:

**`<head>` Content**
Meta tags, title, CSS inclusion, etc

```
head_all
  head_site_meta
  head_opensearch
  head_page_meta
  head_page_title
  head_page_css
  javascript
  head_item_metadata
  head_extra
```
**`<body>` Content**

Navigation, actual content of a given page, and footer

```
body_content
  header
    header_title
    navbar
      navbar_home
      navbar_pos1
      navbar_pos2
      navbar_pos3
      navbar_pos4
      navbar_pos5
      navbar_advancedsearch
      navbar_search
  breadcrumbs
  content
    page_head_container
      page_head
        sub_page_head
    main_content
    subcontent
footer
```

## CSS Customization

If you wanted to overwrite the `boostrap.min.css` file with your own, you could drop it into:

```
- themes
  - YOUR_THEME_NAME_HERE
    - static
      - vendor
        - bootstrap
          - css
            - bootstrap.min.css
```

This may be useful if you want to compile your own `bootstrap.min.css` using sass or less or the online generator.

## Compile Static Assets

Run these commands as a regular user rather than root

```bash
cd /opt/openoni
source ENV/bin/activate

./manage.py collectstatic -c

# Grant write access for both Apache and group
sudo chown -R apache static/compiled/
sudo chmod -R g+w static/compiled/
```

Perform a graceful Apache restart after re-compiling static assets so the app
uses the updated static file hash fingerprints in the URLs rendered in
templates:

```bash
sudo apachectl graceful
```
