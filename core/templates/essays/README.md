## Essays

You may add an essay to a particular title in two ways.  For those moving from the chronam software to Open ONI, Open ONI maintains support for pulling HTML essays stored in the database.  If no associated database record is found, however, Open ONI will search for a template with a matching LCCN.  It is recommended that new users rely on templates for essays for ease of editing and version control.

If a database record and template match the same LCCN, only the first essays in the database will be displayed.  However, there is no restriction on storing some essays in the database and others in the templates for different LCCNs.

### Database Storage

Storing essays in the database is not recommended and no essay loading utility for new essays is provided in Open ONI. If you are moving from chronam to Open ONI and your essays are already stored in the database, your essays should appear on the title page out of the box.

Should you need to add new essays for testing purposes, you can use the following clauses in a mysql terminal, where nbu below is substituted to be your awardee code:

```
INSERT INTO core_essay (title, html, creator_id) VALUES("Title", "<p>Paragraph 1.<p><p>Paragraph 2.</p>", "nbu");
```

Find the `id` of the essay you just added (3 in this example), then associate it with a particular LCCN:

```
INSERT INTO core_essay_titles (essay_id, title_id) VALUES(3,"sn83045462");
```

### Templates

Essays added as a template must have a filename which exactly matches the title's LCCN in the `ESSAY_TEMPLATES` location.  Check your configuration for the `ESSAY_TEMPLATES` setting.  By default, this is usually `"essays"`.  This path applies to all themes / django `INSTALLED_APPS`.  For example, if your configuration contains:

```
INSTALLED_APPS = (
  ...
  'themes.nebraska',
  'themes.default',
  'core'
)

ESSAY_TEMPLATES = "essays"
```

You could add essays in the following directories, keeping in mind that **it is recommended to include essays in your custom "theme" application rather than adding them to the core or default apps!**

```
core/templates/essays/              # no
themes/default/templates/essays/    # okay, if you do not have a custom theme
themes/nebraska/templates/essays/   # recommended
```

If you have one essay for one title, then it is relatively simple to include an essay:

```
# <app>/templates/essays/sn99021999.html

<h4>Essay Title</h4>

<p>This is an essay about the <em>Omaha Daily Bee</em>.</p>
```

In the case that an essay applies to more than one title, you can avoid duplication by including the shared portion of the essay with the django `{% include "path" %}` tag.  Make sure that you use the "full" path from the `templates` directory in your include tag.

```
# themes/nebraska/templates/essays/sn96080312.html

<h4>The Daily Nebraskan</h4>

{% include "essays/shared/hesperian.html" %}
```

```
# themes/nebraska/templates/essays/sn96080314.html

<h4>The Hesperian</h4>

{% include "essays/shared/hesperian.html" %}
```

```
# themes/nebraska/templates/essays/shared/hesperian.html

<p>The Daily Nebraskan, the independent student newspaper at the University of Nebraska-Lincoln (UNL), was founded in 1871 as the Monthly Hesperian Student [LCCN: sn96080317].</p>
```

One benefit of adding the essays to templates is that you have the full power of django templating at your disposal.  You may use django helpers for images, links, block overriding, or whatever else you may need.

Be aware, if you are overriding the behavior in `title.html`, you should include the `template_exists` filter to prevent errors when including a template file which does not exist.

```
{% if essay_template|template_exists %}
    {% include essay_template %}
{% endif %}
```
