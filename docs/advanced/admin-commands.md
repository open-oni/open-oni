# Admin Commands

This document is in progress.

Open ONI offers several dozen management commands which can be used for tasks
such as loading batches, reindexing Solr, and adding titles. These commands
were inherited from the chronam software project and are not all supported.

All the available commands are listed below, but documentation is only
provided for those which Open ONI supports.

Before running commands, activate your environment from your app (not necessary if using docker):

```bash
source ENV/bin/activate
```

- batches
- commit_index
- delete_cache
- diff_batches
- dump_ocr
- ethnicities_with_issues
- index
- index_pages
- index_titles
- link_places
- [load_batch](#load_batch)
- load_batches
- load_copyright
- load_copyright_map
- load_titles
- make_countries_fixture
- process_coordinates
- purge_batch
- purge_django_cache
- purge_etitles
- reconcile
- setup_index
- update_has_issues
- update_sitemap
- zap_index

## load_batch

Ensure that your batch location is a directory containing a `data` directory.

```bash
manage.py load_batch /path/to/batchname
```
With docker, a path is not needed if your batch is in `data/batches`:

```
docker-compose exec web /load_batch.sh batch_name 
```
