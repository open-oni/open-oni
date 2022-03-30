# Admin Commands

Open ONI offers several dozen management commands which can be used for tasks
such as loading batches, reindexing Solr, and adding titles. These commands
were inherited from the chronam software project and are not all supported.

Before running commands, activate your environment from your app:

```bash
# For linux and Mac
source ENV/bin/activate
./manage.py [command]
```

```powershell
# For windows
.\ENV\bin\activate.ps1
```

If using docker, be sure that your docker daemon is running and you have run `docker-compose up`.

If using docker, the `manage` shortcut is necessary.  It automatically
activates the environment, but also fixes some permissions issues which occur
when running `manage.py` as a non-Apache user.

```bash
docker-compose exec web manage [command]
```

Please bear in mind that we are still working our way through some of the
commands and have not yet determined which tasks are no longer useful and
should be removed or which ones need better explanations and support.  Commands
listed below should only be considered supported for long-term use if they
explicitly say so.

## Command-line help

Note that the commands which we support should always have extensive help,
e.g.:

```bash
# Get help on the "load_batch" command
./manage.py help load_batch

# Or with docker
docker-compose exec web manage help load_batch
```

## The Comprehensive List

### To be removed

These are commands which don't get used and just make the list of commands
confusing for no reason.  They will be removed for 1.0 or else very shortly
after its release.

- `batches`
- `commit_index`
- `delete_cache`
- `link_places`
- `purge_etitles`
- `reconcile`

### Unsupported

These may be removed, or they may become supported depending on ongoing work
and discussions.

- [`diff_batches`](#diff_batches)
- `dump_ocr`: Creates OCR dump tarballs (compressed with bzip) for each batch.
  This can use *a lot of storage*, and it can take **a very long time**.
- `ethnicities_with_issues`: Displays a list of ethnicities and "True" or
  "False" indicating if that ethnicity is represented in the collection.
- `load_batches`: Runs the `load_batch` command for each batch in a given file.
- `make_countries_fixture`: Loads MARC Country list XML from the web, and dumps
  JSON fixture to stdout.  *Seems to be broken.*
- `process_coordinates`: Rebuilds a batch's coordinates file; unless a batch
  ingest goes horribly awry *and* you can't reingest said batch, this shouldn't
  need to be run.
- `update_has_issues`: Fixes titles that are not reporting issues.  This
  shouldn't need to be run unless data is being inserted into the database
  manually.
- `update_sitemap`: Creates a sitemap for search engines, but currently this
  functionality isn't complete.  We will potentially improve this command in
  the future, but for now it has to be considered unsupported.

### Supported

These commands will see continued maintenance and support in Open ONI for the
foreseeable future.

- [Indexing commands](#indexing) (`index`, `index_pages`, `index_titles`,
  `setup_index`, and `zap_index`)
- [`load_batch`](#load_batch)
- [`load_copyright`](#load_copyright)
- [`load_copyright_map`](#load_copyright_map)
- [`load_titles`](#load_titles)
- [`purge_batch`](#purge_batch)
- [`purge_django_cache`](#purge_django_cache)

## `diff_batches`

Given a file with batch names, shows a list of batches and an indicator of
their status relative to the current system's batch list.  If a batch is in the
system but not in the file, it is prefixed with a plus `+`.  If a batch is in
the system and the file, it is prefixed with a space ` `.  If a batch is not in
the system but is listed in the file, it is prefixed with a minus `-`.

e.g., given the following batches loaded:

```
batch_dlc_manyyears_ver01
batch_mnhi_german_ver01
batch_nbu_manyissues_ver01
```

And a file called `batch_list` with the following:

```
batch_dlc_manyyears_ver01
batch_nbu_manyissues_ver01
batch_oru_foo_ver01
```

The command `diff_batches batch_list` would print this:

```
 batch_dlc_manyyears_ver01
+batch_mnhi_german_ver01
 batch_nbu_manyissues_ver01
-batch_oru_foo_ver01
```

## Indexing

There are five commands used to manage the Solr index.  Roughly in order of
need, they are as follows.

### Setup

`setup_index` **must** be run when the application is first being set up.  It
verifies that Solr is initialized with the `openoni` core, then tells Solr
about all the fields we use, and configures Solr in a way that works for Open
ONI's needs.  If this is not run, ONI *will not function*.

### Updating

`index` rebuilds the entire title and page index data in Solr, including the
page OCR data.  It shouldn't be necessary most of the time, but it can be
useful to run if Solr data becomes corrupt (though this is a very rare
occurrence), or in cases the Solr index must be deleted, e.g., if you upgrade
to a new major version of Solr.

*If Solr corruption is suspected, you should run the `zap_index` command
prior to reindexing.*

This command can take a while to run, because every single page has OCR data
which Solr has to index in order to facilitate full-text searching.  Plan for
60 to 90 minutes per 100,000 pages in your collection.

Reindexing is considered a stable process for ONI: if you run it once, on a
specific version of Solr, running it again on the same version of Solr will
yield the same outcome.  e.g., search results are expected to be the same.

`index_pages` is a subset of `index`.  It skips the reindexing of titles, but
does all individual issues and pages.  Skipping titles doesn't save much time,
so this is rarely necessary.

`index_titles` is the other half of `index_pages`.  Titles tend to be very few
in an ONI installation, and they contain very little data, so this operation is
usually done in under a minute.

### Removal

`zap_index` **destroys all data** indexed in Solr.  This should not be used
unless you fully understand the ramifications of this!  Without the Solr index,
*most of the site functionality will not work*.

Typically `zap_index` would only be run prior to a full reindex - either
because you suspect corrupted indexes in Solr (this is very rare), or because
you have manually altered the Solr index outside of ONI and need to rebuild it
from scratch.

## `load_batch`

This ingests a batch of newspaper pages, as described in the
[Load and Purge Batches documentation](/docs/manage-data/batches-load-purge.md#load-batch).

## `load_copyright`

Adds copyright URIs and labels for displaying on titles that aren't public
domain.  This must be used with [`load_copyright_map`](#load_copyright_map).

Rights statements files must be tab-separated files where each line contains a
single copyright statement's data in the format of URI followed by a [TAB]
followed by a label.  e.g.:

```
http://www.europeana.eu/rights/rr-f/	Rights Reserved - Free Access
http://creativecommons.org/licenses/by/4.0/	Attribution 4.0 International (CC BY 4.0)
http://creativecommons.org/licenses/by-nc/4.0/	Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
http://creativecommons.org/licenses/by-nc-nd/4.0/	Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
```

Please note that loading the same file multiple times will result in duplicated
data, and manual SQL may be needed to clean dupes from `core_copyright`.

## `load_copyright_map`

Defines rules for which titles should use a given rights statement for certain
date ranges.  Rights *must* first be loaded via
[`load_copyright`](#load_copyright).

Rules are composed of four-field tab-separated-values files, where each line
indicates a single rule.  The fields, in order, are LCCN, start date, end date,
and rights URI.  Start and end dates must be formatted as `YYYY-MM-DD`, e.g.,
`2001-09-08` means September 8th, 2001.

An example rules file might look like this:

```
sn83045462	1922-01-01	1999-12-31	http://creativecommons.org/licenses/by-nc/4.0/
sn83045462	2000-01-01	2999-12-31	http://www.europeana.eu/rights/rr-f/
```

Please note that loading the same file multiple times will result in duplicated
data, and manual SQL may be needed to clean dupes from `core_lccndatecopyright`.

## `load_titles`

Loads titles into Open ONI from a single file or a path containing multiple
files.  All files must contain valid MARC XML.

A typical example might look like this:

```bash
./manage.py load_titles /var/local/marcxml
```

You can aggregate custom / overridden MARC XML in a single place and run a
command like this as often as necessary; titles which already exist will not be
reimported.  (If you *need* to overwrite a title, there is unfortunately no way
to do so with administrative commands.)

## `purge_batch`

This removes a previously-ingested batch, as described in the
[Load and Purge Batches documentation](/docs/manage-data/batches-load-purge.md#purge-batch).

## `purge_django_cache`

Removes the cache of newspapers' title data - this should typically not need to
be run manually, but can be necessary when the site isn't reflecting a recent
batch ingest or purge.
