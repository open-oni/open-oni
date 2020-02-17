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
- [load_titles](#load_titles)
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

This command loads the metadata and pages associated with a batch into a
database and search index. It may take up to several hours to complete,
depending on the batch size and machine. If there is a chance of interruption
to where the command is running (for example, on a remote machine), you may
wish to preface the command with `nohup` in order to ensure the batch will be
completed regardless of your connection.

Ensure that your batch location is a directory containing a `data` directory.

```bash
manage.py load_batch /path/to/batch_name
```
With docker, a path is not needed if your batch is in `data/batches`:

```bash
docker-compose exec web /load_batch.sh batch_name 
```

## load_titles

Documentation pending.

## purge_batch

This command removes pages associated with a batch from the search index and
database, but does not remove titles specific to this batch. It is effective
even on batches which were only partially loaded.

```bash
manage.py purge_batch batch_name
```

With docker:

```bash
docker-compose exec web manage purge_batch batch_name
```
