# Load and Purge Batches

The load and purge batch explanations are copied from the
[admin commands](/docs/advanced/admin-commands.md) documentation.

- [Load Batch](#load-batch)
- [Purge Batch](#purge-batch)
- [Obtain Batches](#obtain-batches)

If you are using docker, batches should be stored in `data/batches`.

## Load Batch

This command loads the metadata and pages associated with a batch into a
database and search index. It may take up to several hours to complete,
depending on the batch size and machine. If there is a chance of interruption
to where the command is running (for example, on a remote machine), you may
wish to preface the command with `nohup (command) >> nohup.out` in order to
ensure the batch will be completed regardless of your connection.

Ensure that your batch location is a directory containing a `data` directory.

```bash
source ENV/bin/activate
manage.py load_batch /path/to/batch_name
```

If you are having trouble viewing images / documents after loading your batch,
you may want to check your permissions. The following are permissive enough to
allow reading files for the image server, text, etc:

```
cd /path/to/batch_name

sudo chmod -R g+rwX
sudo chmod -R o+rX
```

With docker, a path is not needed if your batch is in `data/batches`:

```bash
docker-compose exec web /load_batch.sh batch_name
```

After ingesting a batch that replaces existing content it is recommended 
to restart the web server to clear caches and serve the most up to date 
data. 

## Purge Batch

This command removes pages associated with a batch from the search index and
database, but does not remove titles specific to this batch. It is effective
even on batches which were only partially loaded. Data that was purged may
continue to serve from the cache. It is recommended to restart
the web server after purging a batch to clear the residual cache.

```bash
source ENV/bin/activate
manage.py purge_batch batch_name
```

With docker:

```bash
docker-compose exec web manage purge_batch batch_name
```

## Obtain Batches

There are a number of ways to obtain batches if you find yourself short of
data.

You can [download a sample batch](https://github.com/open-oni/sample-data) ,
which are small example sets we use for testing.

You can also copy a batch from the Library of Congress's collection. This will
take some time. Please alter the path `/data/batches/` to the location of your
batches. You can browse available batches at
https://chroniclingamerica.loc.gov/batches/.

```bash
cd data
wget --recursive --no-host-directories --cut-dirs 1 --reject index.html* \
     --include-directories /data/batches/batch_uuml_thys_ver01/ \
     https://chroniclingamerica.loc.gov/data/batches/batch_uuml_thys_ver01/
```
