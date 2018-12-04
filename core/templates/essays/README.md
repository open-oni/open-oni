## Essays

Essays are included automatically on a newspaper's title page if there is a file in this directory (or the settings.ESSAY_TEMPLATES directory) matching the title LCCN.  For example, the webpage 'lccn/sn99021999' would provide you information about the Omaha Daily Bee and include an essay in `themes/nebraska/templates/essays/sn99021999.html`.

**It is recommended to include essays in a "theme" application rather than adding them in this directory!**

If you are overriding the behavior in `title.html`, you are encouraged to include the `template_exists` filter to prevent errors when including a template file which does not exist.

Example essay:

```
# <app>/templates/essays/sn99021999.html

<h4>Essay Title</h4>

<p>This is an essay about the <em>Omaha Daily Bee</em>.</p>
```

## Essays with Multiple Titles

In the case that an essay applies to more than one title, you can avoid duplication by including the shared portion of the essay with the django `{% include "path" %}` tag.  Make sure that you use the "full" path from the `templates` directory in your include tag.

```
# <app>/templates/essays/sn96080312.html

<h4>The Daily Nebraskan</h4>

{% include "essays/shared/hesperian.html" %}
```

```
# <app>/templates/essays/sn96080314.html

<h4>The Hesperian</h4>

{% include "essays/shared/hesperian.html" %}
```

```
# <app>/templates/essays/shared/hesperian.html

<p>The Daily Nebraskan, the independent student newspaper at the University of Nebraska-Lincoln (UNL), was founded in 1871. Because it is a student newspaper, it uniquely views major events through the lens of university life. Upon its founding, the newspaper now nicknamed "the DN" was first called the Monthly Hesperian Student [LCCN: sn96080317] and published by the Palladian Literary Society, a student group.</p>
```
