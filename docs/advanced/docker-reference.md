# Docker Command Quick Reference

This list may not be comprehensive, but we hope it's a good start for those new
to docker and Open ONI.

- [Rebuild Dev Containers](#rebuild-dev-containers)
- [Manage Data](#manage-data)
- [Run Commands from Containers](#run-commands-from-containers)
- [Django Reference](#django-reference)
- [Manage Containers, Volumes, and Images](#manage-containers-volumes-and-images)

## Rebuild Dev Containers

Builds or rebuilds the development setup.  Useful if you changed something
copied into the container, such as the various helper scripts in the `docker`
directory:

```bash
docker-compose down
docker-compose up
```

Or if you don't want to be "trapped" in the log output: `docker-compose up -d`

Remember, you can always get at logs via `docker-compose logs`, and drill down
just to the logs you want, which is usually the web service: `docker-compose logs web`.

## Manage Data

### Load a Batch

If you do not already have a batch ready to load, you can learn about how to
obtain a batch in the [Load and Purge Batches documentation](/docs/manage-data/batches-load-purge.md#obtain-batches).

Then run our custom batch-loader wrapper:

```bash
# You have to have the services running in order to ingest
docker-compose up -d

docker-compose exec web /load_batch.sh <batch_name>
```

`/load_batch.sh <batch_name>` is a shortcut for:

```bash
manage load_batch /opt/openoni/data/batches/<batch_name>
```

And `manage` is a custom wrapper for the Django `manage.py` script, but it
fixes permissions so that any operations which alter the filesystem cache will
still be readable when the Apache user tries to read them.

### Purge a Batch

```bash
docker-compose exec web manage purge_batch batch_uuml_thys_ver01
```

## Run Commands from Containers

Open ONI app shell:

```bash
docker-compose exec web bash
```

Database shell:

```bash
docker-compose exec rdbms mysql -uroot -p123456 -Dopenoni
```

Django shell:

```bash
docker-compose exec web manage shell
```

Then work with the Django ORM like this:

```python
from core import models
models.Titles.objects.all()
```

## Django Reference

### Run tests

```bash
docker-compose -f test-compose.yml -p onitest up test
```

The test container definition runs a shortcut for unit tests with a special
settings file for forcing in reproducible URLs and ensuring a very "clean",
consistent environment.

Remove all test containers, volumes, and images with the following command:

```bash
docker-compose -f test-compose.yml -p onitest down -v --rmi local
```

### Rebuild static files

These include CSS, JS, and images. You will need to run this command when
developing themes:

```bash
docker-compose exec web manage collectstatic --noinput
```

### Run arbitrary admin commands

`django-admin` is available within the container:

```bash
docker-compose exec web django-admin help
```

Note that django-admin doesn't know about specific projects without passing the
--settings flag.  Instead, use `manage`, which is an alias to the `manage.py`
script within the Open ONI project:

```bash
docker-compose exec web manage help batches
```

### Change / update Python dependencies

If `requirements.pip` is changed or you want to update dependencies in
`requirements.lock`, you'll need to run `pip-update.sh`. The `pip-install.sh`
and `pip-reinstall.sh` scripts install from `requirements.lock`.

```bash
docker-compose exec web /pip-update.sh
```

### Django Migrations in Docker

Roll back the database

```bash
docker-compose exec web manage showmigrations
docker-compose exec web manage migrate <app (core)> <migration name>
```

## Manage Containers, Volumes, and Images

Remove the containers (persistent data remains)

```bash
docker-compose down
```

Remove persistent data containers and data volumes

**NOTE**: Only do this if you want to restart with no data!

```bash
docker-compose down
docker volume rm open-oni_data-mariadb
docker volume rm open-oni_data-solr
```

### Containers

```
docker ps -a              # all containers, including stopped
docker ps                 # all running containers
docker rm container_id    # remove container (if stopped)
docker rm container_name  # remove container (if stopped)
```

### Data Volumes

```
docker volume ls                   # list all data volumes
docker volume ls -f dangling=true  # list data volumes not associated with a container
docker volume rm volume_name       # delete data volume
```

### Images

```
docker images             # list images
docker rmi image_name      # delete an image (need to remove containers, first)
```

### Stop the Open ONI Stack

```bash
docker-compose down
```
