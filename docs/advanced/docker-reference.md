# Docker Command Quick Reference

This list may not be comprehensive, but we hope it's a good start for those new
to docker and Open ONI.

- [Rebuild Dev Containers](#rebuild-dev-containers)
- [Manage Data](#manage-data)
- [Run Commands from Containers](#run-commands-from-containers)
- [Django Reference](#django-reference)
- [Manage Containers, Volumes, and Imges](#manage-containers-volumes-and-images)

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

You will need to put NDNP-compliant newspaper batches in the `data/batches`
directory at the root of the project.  You can either wget a batch from
Chronicling America like below, or you can put some of our [short sample
batches](https://github.com/open-oni/sample-data) into the data directory.

Mirroring a batch from Chronicling America is easy, but can take a *lot* of time:

```bash
cd data
wget --recursive --no-host-directories --cut-dirs 1 --reject index.html* \
     --include-directories /data/batches/batch_uuml_thys_ver01/ \
     https://chroniclingamerica.loc.gov/data/batches/batch_uuml_thys_ver01/
cd ..

# You have to have the services running in order to ingest
docker-compose up -d
```

Then run our custom batch-loader wrapper:

```bash
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

This is essential for theme development:

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

### Change dependencies

If requirements.pip is changed, you'll need to run the pip reinstall in the container:

```bash
docker-compose exec web /pip-reinstall.sh
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
docker rm image_name      # delete an image (need to remove containers, first)
```

### Stop containers and Docker VM

```bash
docker-compose down
```
