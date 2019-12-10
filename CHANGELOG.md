# Open ONI Changelog
All notable changes to Open ONI will be documented in this file.

Starting from Open ONI v0.11, The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- Template - Please preserve this order of sections
## [Unreleased] - Brief description
[Unreleased]: https://github.com/open-oni/open-oni/compare/v#.#.#...dev

### Fixed

### Added

### Changed

### Removed

### Migration

### Deprecated

### Contributors
-->

## [Unreleased] - Python 3 and Django 2.2 upgrades
[Unreleased]: https://github.com/open-oni/open-oni/compare/v0.11.1...dev

### Fixed
- Sitemap Apache alias paths

### Changed
- All code in ONI core, including the default theme, has been migrated to work
  with Django 2.2 LTS
  - Django 2.2 only supports Python 3
    - Python 2 code will no longer work anywhere in the stack: plugins, themes,
      core overrides, etc.
  - The docker setup installs a much newer Ubuntu server as well as Python 3.6
- Docker-compose changes:
  - MariaDB and Solr ports are no longer forcibly exposed to the host
    - If you need these, use a `docker-compose.override.yml` file
  - Batches must now live under `./data/batches`, not `./docker/data/batches`
    for ingest
    - This fixes odd issues which can occur when mounting over an existing
      mount point (we mount `.` as `/opt/openoni`, and previously were mounting
      `./docker/data` as `/opt/openoni/data`, effectively shadowing the actual
      data directory)
  - All generated ingest artifacts now live in a named volume, `onidata`, which
    is mounted into multiple containers as `/var/local/onidata`

### Removed
- All Python 2 support / compatibility
- The concept of "released" batches has been removed to reduce confusion:
  ingested batches become part of the system regardless of their "released"
  status, and are simply not displayed on the (undocumented) `/batches` list.
  This is extremely confusing and not terribly helpful, so we've opted to
  simply remove the feature entirely.  All batches are now live upon ingest
  (which, again, they always were, it just wasn't terribly obvious).

### Migration
- If you use any of our plugins, make sure you look over their repositories and
  get a version that is built for Django 2.2.  Django 2.2 only supports Python
  3, so plugins which work with Django 2.2 will work with Python 3.
  - Plugins built by the ONI team should generally include compatibility
    information in their README; here's [our calendar plugin's
    information](https://github.com/open-oni/plugin_calendar#compatibility), for
    example.
- Custom themes and plugins you've built will need to be fixed for Django 2.2,
  and therefore Python 3
  - Exact fixes are out of scope for ONI, but you can learn a lot from:
    - The [Python porting
      documentation](https://docs.python.org/3/howto/pyporting.html)
    - The [2to3](https://docs.python.org/2/library/2to3.html) tool's
      documentation
    - The [Django upgrade
      documentation](https://docs.djangoproject.com/en/2.2/howto/upgrade-version/)
  - Most themes and plugins will need minimal work to get updated, but complex
    Python code could require a lot of migration effort
- Move your local/development batches into `./data` if you previously had them
  in `./docker/data`
- If you use docker with a custom configuration, make sure you mount `onidata`
  into your `web` container in the same place your Apache configuration is
  expecting to find word coordinates.

### Deprecated
- [Django Deprecation
  Timeline](https://docs.djangoproject.com/en/2.2/internals/deprecation/)
- MariaDB and Solr will be upgraded for Open ONI 1.0, so existing databases and
  Solr indices will have to be repopulated

### Contributors
- Jessica Dussault (jduss4)
- Jeremy Echols (jechols)
- Greg Tunink (techgique)

## [v0.11.1] - Hotfix for word coordinates and image viewer
[v0.11.1]: https://github.com/open-oni/open-oni/compare/v0.11.0...v0.11.1

### Fixed
- Bug in the word coordinate location has been fixed for docker-compose users
- Fixed RAIS (IIIF server) setup in docker-compose

### Contributor
- Jeremy Echols (jechols)

## [v0.11.0] - Django 1.11 LTS Upgrade, Production Docs, and Feature Updates
[v0.11.0]: https://github.com/open-oni/open-oni/compare/v0.10.0...v0.11.0

### Fixed
- Language filtering test
- Solr code's SolrPaginator `_count` attribute presence check
- Use `_logger` for logging calls
- Batch loading in `batch_loader.py`
  - Bulk foreign key handling
  - Handle unreliable path comparison due to trailing slash
  - Handle if `BATCH_STORAGE` path is a symlink
- Invalid static tag use to render static URL in `page.html` data attributes
- The docker-based test setup should now function properly

### Added
- This changelog, with all previous releases
- CentOS 7 deployment documentation in `docs/` and config files in `conf/`
- `navbar_classes` template block in `__base.html`'s
  `<nav class="navbar …"` attribute
- Year filter and language filter selects on search results pages
- Multiple template blocks in `search_pages_results.html`, `newspapers.html`,
  and `page.html`
- Template block around link to batch on issue page
- Date filtering tests
- `pip-reinstall.sh` script to reinstall Python virtual environment and pip
  dependencies and restart Apache
- Load batch management command help text and batch existence check with error
  message
- Comments in `docker/_startup_lib.sh` that identify `.env` file as source of
  environment variables used for configuration
- Strict mode use in MariaDB/MySQL via `sql_mode = TRADITIONAL`
- Configuration boolean for whether title name displays medium in parentheses,
  e.g. "(volume)" or "(microform)"
- `custom_size_image_url` template tag for requesting custom image sizes
- On-page JavaScript newspaper title filtering on `newspapers.html`
  - Rearrange layout of title / page counts and filter input with Bootstrap
- `strftime_safe` method in `core/utils.py` to print years before 1900
  - Alias `core.utils.strftime` to this function for backwards compatibility
  - Replace direct calls to `datetime_safe.new_datetime` with `strftime_safe`

### Changed
- Upgrade Django from 1.8 LTS to 1.11 LTS
  - [Full release notes](https://docs.djangoproject.com/en/1.11/releases/) for
    reference
  - pip dependencies updated as well
    - Version constraint on rfc3339 removed - library still maintained and
      updates are compatible
  - Pass `MiddlewareMixin` to middleware class definitions for compatibility
    with `MIDDLEWARE` setting change from `MIDDLEWARE_CLASSES`
  - Replace `render_to_response` with `render` in view code
- Update Bootstrap to 3.4.1
- Update OpenSeadragon to 2.4.1
- Update jQuery tablesorter to 2.31.1
  - Change toggle for using title sort parser to `sort-titles` class on <th>
    element, rather than defaulting to first column
  - Change toggle for disabling sort to `sort-off` class on <th> element, rather
    than defaulting to fourth column
  - Update template to use new toggle classes
  - Update tablesorter css; Use default cursor on unsorted column header
  - Move initializing JavaScript on `newspapers.html` to external file
    `newspapers.js`
- Update jQuery to 3.4.1
  - Remove jQuery CDN loading; replace with local copy of jQuery 3.4.1
  - Move JS libraries loading from bottom of `<body>` back into `<head>`
  - Remove conditional loading of now missing HTML5 shim
  - Update JavaScript use across all templates
    - Move javascript template block to top of files
    - Update jQuery on-DOM-load ready syntax
    - Improve multiple issue JS for non-plugin calendar
      - Make minimally keyboard-accessible
- `README.md` updates
  - Link to GitHub wiki and releases
  - Recommend installing from latest release to evaluate software and
    checking out `dev` branch for contributing changes
  - Simplify section blurbs and link to wiki pages for more information
  - Add "Support" section outlining support expectations
  - Add list of Open ONI-powered sites
  - Update Markdown syntax and reorganize sections
  - Add link text communicating which links navigate to the wiki
- Docker / Apache / deployment script changes
  - Set Django code Docker bind mount volume to shared-across-containers
    SELinux label
  - Pip updates itself before installing dependencies, now much more quickly
  - Create and destroy database for each test run
  - Dump OCR management command no longer relies upon celery, enabling removal
  - Serve word coordinates files through Apache, bypassing Django
  - Update Apache config every time web container starts rather than only
    during Docker image creation
- Update and reorganize Django settings files
  - Begin with the default config generated for a new Django app in
    `django_defaults.py`
  - Only environment-independent settings in `settings_base.py`
  - Include default list with commented omissions and additions in overrides
  - Use default enabling of i18n, l10n, and timezone support set to UTC zone
  - Remove some defaults included in overrides but not changed, e.g.
    `STATIC_URL`
  - Retain session, messages, and security middleware previously omitted
  - Change compiled static assets path `STATIC_ROOT` to `static/compiled`
      - Update corresponding Apache config
  - Put settings that shouldn't change for dev / production environments in
    separate files `settings_development.py`, `settings_production.py`
      - Development environment
          - Disable client-side caching via custom middleware
          - Use console output email backend
          - Change Apache WSGI config to reload the app after every request so
            multiple processes and threads don't persist and render page
            contents based on cached versions of the code base
      - Production environment
          - Switch static file storage class from `CachedStaticFilesStorage`
            to `ManifestStaticFilesStorage` for performance and graceful
            Apache restart compatibility
  - Move commonly changed settings to `settings_local_example.py`
      - Place env-independent settings at the top
      - Default to dev environment
      - Include unchanging settings for environments from separate files
      - Collect settings which seem more likely to be changed for production
      - Comment out all production settings; add instructions on how to use
      - Add disabled-by-default SQL logging config which doesn't disable other
        loggers to dev environment settings
      - Differentiate `YOUR_` strings for possibly differening web, database,
        and Solr hosts; log and data paths
      - Add optional debug file logging config
      - Add email settings for host, from, subject, etc with guiding comments
      - Copy file to `settings_local.py` during Docker container creation
  - Review [Django deployment
    checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/)
    and add settings to remove warnings from `manage.py check --deploy`
    - Add MIME-type sniffing prevention header in `settings_base.py`
    - Add broken link email middleware in `settings_production.py` and related
      toggling settings in `settings_local_example.py`
    - Add database connection re-use setting in `settings_local_example.py`
    - Add CSRF, secure cookie, `SECURE_SSL_REDIRECT` settings;
      collectHTTPS/HSTS-related settings together in `settings_local_example.py`
    - Add `X_FRAME_OPTIONS = 'DENY'` to `settings_base.py`
  - Update `urls_example.py` with Django recommendation to use raw strings
    and comments to guide plugin, theme, and core Open ONI URL includes
- Update tests to pass; Remove system tests
  - Modify times in fixture JSON to TZ-aware format with UTC times
  - Remove system tests as Django and Python dictated/tracked elsewhere
  - Make datetime objects TZ-aware in `title_loader`, `test_ocr_dump`
  - Update timestamps in JSON tests to match UTC format
  - Update IIIF manifest JSON tests to match updated manifest format
- Improve search page results layout / functionality
  - Date range search handling refactored
    - dateFilterType param removed; yearRange supercedes date1 and date2
  - Solr query won't pass query params for dates if no date filtering
    requested
  - Remove `form-inline` class so selects display below related labels
  - Shorten "Jump to page" input field
  - Move "Front pages only" check left of submit
  - Add space above checkbox and submit button
  - Move "Refine search" button to right to align with other controls
  - Move filters and result numeration above pagination controls
  - Move result count above filter controls
  - Move pagination controls to separate template and include both above and
    below results
  - Move gallery/list display control to left, pagination controls right
  - Don't display pagination or result template blocks if no results
  - Don't display pagination controls if only one result page
  - Fix pluralization and "No matches found" text with result counts
  - Remove duplicate text and update spacing in list view-specific template
  - Improve filter removal controls
    - Change controls to inline list with Bootstrap buttons
    - Display truncated title of paper rather than just LCCN value
    - Drop removal button redundant to year filter select
    - Only show removal for date range filter from Advanced Search if overriding
      year filter select not in use
    - Update hidden inputs to retain filter values across form submissions
    - Clarify date filter removal text to communicate whether both fields are
      populated or only a From date or Until date present
  - Don't include highlight words param in pagination URLs where not necessary
    - Only add param if highlight words present
- Advanced Search improvements
  - Search any Solr language present in newspaper titles which have issues
  - Date range inputs are now native date inputs, `type="date"`
    - Back end code updated to handle YYYY-MM-DD format sent to the server
    - Related tests updated
    - Set initial values to site-wide min and max; bypass inclusion in Solr
      query if unmodified from these values
      - This requires default values pass through as GET parameters upon form
        submission; Hide date filter removal link when these default values are
        not actually filtering
    - Update styling to give date inputs more width for easier use and display
      date limits for site's newspapers closer to inputs
  - Update newspaper title multi-select
    - Re-write label and instructions for clarity
    - Remove "All newspapers" option which results in error
- Page viewer changes
  - Specify issue date on button to view entire issue
  - Improve overlapping and spacing around viewer controls; Make more consistent
    across browsers
  - Update page and issue controls to display message when no pagination
  - Add aria-label and aria-hidden attributes to improve screen reading
  - Add "Return to Top" link at bottom left
  - Copy page and issue pagination controls at bottom right; Add necessary
    related JS
- Modernize issue pages, batches report pagination
  - Wrap pagination controls in Bootstrap row
  - Add margin below pagination control row
  - Adapt pagination template from search results
  - Add page variables in view code
  - Convert some dev comments to template comments
  - Make previous/next issue links Bootstrap buttons
- Newspaper titles page (`newspapers.html`) updates
  - Site-wide page count total above newspaper title table
  - Fix typo using `<th>` elements in the table body
- Issue page changes
  - Handle issues with no pages in `issue_pages.html` and associated
    `views/browse.py`
  - "View First Issue" and "View Last Issue" links go to main issue page rather
    than issue first page
- Review and clean `__base.html`
    - Remove templates in theme from core files (__overrides, home, about)
  - Clean up `__base.html` and templates in default theme
    - Reorganize template blocks with sitewide content blocks first
    - Move sitewide meta tags to new template block `head_site_meta`
    - Use site title in OpenSearch titles
    - Set better page title default (page-specific title before site title)
    - Use template-only comments, trim whitespace, 80-character margin
    - Modernize CSS and JavaScript markup (drop extra attributes)
    - Add sitewide skip link and target between template blocks, so less likely
      to be overridden
  - Clean up `__overrides.html` with clearer documentation including block list
    and simpler default overrides for favicon and page meta tags
  - Add generic favicon.png to default theme
- Design consistency
  - Change search / submit / etc buttons to use Bootstrap primary color
  - Title case on button text rather than all letters capitalized
- Clean up CSS files and conditional inclusion
  - Move `main.css` inclusion from `__base.html` into default theme
    `__overrides.html` as `main.css` lives in the default theme
  - Move minimal contents of `a11y.css` into `main.css`
  - Move minimal contents of `highlights.css` into `search.css`
  - Move `tablesort.css` to only be included when necessary
    - Add margin to top of table for space between search input
  - Remove unnecessary `media` attribute from link elements
  - Move dev-only comments to template comment for `page.html` CSS
- Update return to top links with new skip link target `#maincontent`
  - Remove old `#skip_menu` and `.backtotop` class with no related CSS or JS
  - Change all link text to "Return to Top"
  - Remove block elements around links to prevent page-width block elements from
    pushing other nearby controls down
- Remove `required` attribute from Django-generated form fields
- Display essay on newspaper title page if present in database or if file with
  LCCN for name present at configurable `ESSAY_TEMPLATES` path
  - Documentation in ` core/templates/essays/README.md`
- Change SQL to Django ORM for batch issue list to include issues with no pages
- Sort batches report page list by most recently created first
- Update Not Found (404) and Error (500) page templates to remove site title
  variable use and unnecessary CSS classes
- Replace `datetime.now()` calls with timezone-aware `timezone.now()`
- Only load `highlight.js` on `search_pages_results.html`
- Update default theme README instructions for creating a new theme
- Clean up improperly formatted `OpenONI` strings and incorrectly search and
  replaced strings in URLs

### Removed
- Django 1.8 to 1.11
  - Passing (Request)Context objects to template.render
  - `django.conf.urls.patterns` use in `urls.py`
  - `render_to_response` param `context_instance` to render templates at the end
    of view code
  - `optparse` support for custom management commands (replaced by `argparse`)
- celery from `requirements.pip`; Unused Celery management commands
- Load institutions management command - Already loaded in database migration
  from `fixtures/institutions.json`
- Unused setting `PROFILE_LOG_BASE` handling
- Settings overrides from `/etc/openoni.ini`
- Title pull / sync and local holding loading management commands
- Unused variable for removed similar pages links info retrieved from Solr
- Extra `<a>` around "Text" link in page viewer controls
- `newspaper_info` context processor which queried Solr or cache every request,
  but is no longer in use
- Misleading batch link if viewing first pages, as the pages could be from
  multiple batches
- Cities with no issues from nav search's select
  - This can result from batches purged leaving records in the Places table

### Migration

Migrating to v0.11 requires special attention to a lot of changes.  Read this
carefully before attempting a migration, and it may behoove you to read over
the [Django upgrade
notes](https://docs.djangoproject.com/en/2.2/howto/upgrade-version/) if your ONI
instance has a lot of custom code.

- Rewrite your settings **from scratch**.  The new
  `onisite/settings_local_example.py` file should help guide you, but enough
  has changed this release that you can't just copy your old settings and
  expect things to work!
- If you were using a `docker-compose.override.yml` file, update its version to
  2.1
- Django 1.8 to 1.11
  - [Update use of (Request)Context objects passed to `template.render` calls at
    the end of code in view
    definitions](https://docs.djangoproject.com/en/1.11/ref/templates/upgrading/#get-template-and-select-template)
  - [Import `django.utils.deprecation.MiddlewareMixin` in middleware and pass
    `MiddlewareMixin` to middleware class
    definitions](https://github.com/open-oni/open-oni/commit/c51d7235d47690884da00a794c3f522933579925)
  - Remove import of `django.conf.urls.patterns` from `urls.py` files
  - [Replace `render_to_response` with `render` in view
    code](https://github.com/open-oni/open-oni/commit/c40ca4eb87a47865c1d88cb92d3b9d316cea277f)
  - [Convert `optparse` to `argparse` in custom management
    commands](https://github.com/open-oni/open-oni/commit/37854ea135ce011add09040de06506c794e130d0)
- Tablesorter update for `newspapers.html`
  - Add `sort-titles` class on <th> element to toggle use of title sort parser
    which ignores articles "a", "an", and "the"
  - Add `sort-off` class on <th> element to disabling sorting by column(s)
- Review updated `__base.html` and default theme `__overrides.html` to mimic
  inclusion of favicon and default page author + description
  `<meta>` tags
- Update skip links and return to top links to target `#maincontent`

### Deprecated
- Django 1.8 to 1.11
  - [Full deprecation
    timeline](https://docs.djangoproject.com/en/1.11/internals/deprecation/) for
    reference
  - Use of `MIDDLEWARE_CLASSES`, to be removed in Django 2.0
- Python 2's end of life is coming soon, and Open ONI will *no longer
  support it* after this release

### Contributors
- Karin Dalziel (karindalziel)
- Tinghui Duan (via Slack)
- Jessica Dussault (jduss4)
- Jeremy Echols (jechols)
- Linda Sato (lsat12357)
- John Scancella (johnscancella)
- Greg Tunink (techgique)

## [v0.10.0] - 2018-01-29 - Hey it actually really works again!
[v0.10.0]: https://github.com/open-oni/open-oni/compare/v0.9.0...v0.10.0

- Unpinned RAIS for Docker users
- Fixed URL for pulling MARC records from Chronicling America

## [v0.9.0] - 2018-01-24 - Hey it works again!
[v0.9.0]: https://github.com/open-oni/open-oni/compare/v0.8.0...v0.9.0

- Freezes dependencies to fix a problem where new installs would simply not work
  due to missing python libraries
- Updates advanced search to put "Search Terms" above "Proximity Search" based
  on user feedback

## [v0.8.0] - 2017-11-14 - Bug fixes
[v0.8.0]: https://github.com/open-oni/open-oni/compare/v0.7.0...v0.8.0

Adds "proximity" searching back into the advanced search, and improves
accessibility with the search results pagination

## [v0.7.0] - 2017-10-25 - Bug fixes
[v0.7.0]: https://github.com/open-oni/open-oni/compare/v0.6.0...v0.7.0

Multiple bugs have been addressed:
- The "about" page, when the first or last issue wasn't digitized, no longer
  crashes
- The "page number" in advanced search was never working and has been replaced
  with a checkbox to choose front pages only
- The selected titles, from advanced search, now persist when refining search
  results
- The "jump to page" functionality no longer loses various search filters
- Various other "refine search" persistence problems have been addressed

## [v0.6.0] - 2017-09-21 - New languages support, universal viewer support, mariadb
[v0.6.0]: https://github.com/open-oni/open-oni/compare/v0.5.0...v0.6.0

This is a big back-end release:
- We've now got Solr configured to support a bunch of new languages instead of
  just the four or five we had from the chronam fork.
- We've updated the docker setup to use mariadb instead of mysql (you'll
  probably want to dump your MySQL database and import it into MariaDB).
- Last, but definitely not least: there is now significantly better support for
  IIIF systems like the Universal Viewer!

## [v0.5.0] - 2017-09-07 - Bug fixes
[v0.5.0]: https://github.com/open-oni/open-oni/compare/v0.4.0...v0.5.0

- Fixes a failure that affected everybody trying to set up a new ONI site. Oops.
- Adds image attribution on image pages
- Fixes a crash in the title "front pages" view when a published image wasn't
  digitized

## [v0.4.0] - 2017-08-29 - Bug fixes and dev improvements
[v0.4.0]: https://github.com/open-oni/open-oni/compare/v0.3.0...v0.4.0

Highlights finally work properly (we think)!! Also, skip links work better,
there's an easier way to run tests locally via docker, and Apache log level is
configurable by an environment variable.

## [v0.3.0] - 2017-08-24 - Search fixed and slightly better UI
[v0.3.0]: https://github.com/open-oni/open-oni/compare/v0.2.2...v0.3.0

- Improves accessibility on the advanced search form and the search results
  templates
- Removes state dropdowns from advanced search and search results templates
- Removes the redundant link in the titles list ("More Info") for newspapers
  with essays associated

## [v0.2.2] - 2017-08-22 - Faster purge
[v0.2.2]: https://github.com/open-oni/open-oni/compare/v0.2.1...v0.2.2

Removes the solr and mysql optimization as a default step when purging batches,
as it can take a very long time with large datasets. Optimization can still be
done by adding `--optimize` to the purge command.

## [v0.2.1] - 2017-08-11 - Image URL bug fixes
[v0.2.1]: https://github.com/open-oni/open-oni/compare/v0.2.0...v0.2.1

Fixes a bug where resized image URLs were always at the thumbnail size. Adds a
new size option, "tiny", for accommodating smaller devices more effectively.

## [v0.2.0] - 2017-08-09
[v0.2.0]: https://github.com/open-oni/open-oni/compare/v0.1.0...v0.2.0

This release upgrades the docker-compose setup to use Solr 6.6, and fixes a few
bugs only discovered when there were multiple pages of batches

## [v0.1.0] - 2017-07-24
[v0.1.0]: https://github.com/open-oni/open-oni/releases/tag/v0.1.0

This is the official initial release of Open ONI. The changes since forking are
too numerous to try and describe.

