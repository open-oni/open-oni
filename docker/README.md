Docker Open ONI
===============

Install Docker.  We have comprehensive instructions for
[installing Docker on OS X](https://github.com/open-oni/open-oni/wiki/Docker-Setup-OS-X)
on the open-oni wiki.

production
---

(Production instructions TBD - for now this is just for doing open-oni dev)

Open ONI Development
---

Clone this repo, and then clone open-oni inside it:

```bash
git clone https://github.com/open-oni/docker-open-oni.git

# Wait until the clone is finished, then:
cd docker-open-oni
git clone https://github.com/open-oni/open-oni.git
```

### Quick setup

First, please set `APP_URL` to the public URL for your open-oni instance, for
example:

    export APP_URL=http://oregonnews.uoregon.edu

You may want to put that in your `~/.profile` or equivalent so you don't forget
to set it. As a convenience if you are using `docker-machine` on Windows or 
OS X and have named your virtual machine `default` then `dev.sh` will attempt 
to set APP_URL using using the virtual machine's IP address

Now run [`./dev.sh`](dev.sh) which will set up all the containers in order, 
and makes sure the app is ready to run.

For Linux users who can't (or don't want to) expose port 80, the environment 
variable `DOCKERPORT` will override the default of using port 80.

### Manual setup

For more control, you can run the commands manually:

#### Build the app image

```bash
docker build -t open-oni:dev -f Dockerfile-dev .
```

#### Build data containers for mysql and solr

```bash
docker create -v /var/lib/mysql \
  --name openoni-dev-data-mysql mysql
docker create -v /opt/solr \
  --name openoni-dev-data-solr makuk66/docker-solr:$SOLR
```

#### Build mysql and configure it

```bash
docker run -d \
  -p 3306:3306 \
  --name openoni-dev-mysql \
  -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
  -e MYSQL_DATABASE=openoni \
  -e MYSQL_USER=openoni \
  -e MYSQL_PASSWORD=openoni \
  --volumes-from openoni-dev-data-mysql \
  mysql
```

...wait 10-20 seconds for mysql to listen, and then:

```
# Set up the test database permissions
docker exec openoni-dev-mysql mysql -u root --password=$MYSQL_ROOT_PASSWORD -e 'USE mysql;
GRANT ALL on test_openoni.* TO "openoni"@"%" IDENTIFIED BY "openoni";';

# Set the character set
docker exec openoni-dev-mysql mysql -u root --password=$MYSQL_ROOT_PASSWORD -e 'ALTER DATABASE openoni charset=utf8';
```

#### Build solr

This gives us 4.10.4, which is an unofficial docker image, but for now that's
what openoni uses.

```bash
docker run -d \
  -p 8983:8983 \
  --name openoni-dev-solr \
  -v /$(pwd)/solr/schema.xml:/opt/solr/example/solr/collection1/conf/schema.xml:Z \
  -v /$(pwd)/solr/solrconfig.xml:/opt/solr/example/solr/collection1/conf/solrconfig.xml:Z \
  --volumes-from openoni-dev-data-solr \
  makuk66/docker-solr:4.10.4
```

#### Run RAIS

This pulls down and runs the latest RAIS, a tile server optimized for serving
JP2 images:

```bash
docker run -d \
  -p 12415:12415 \
  --name openoni-dev-rais \
  -e PORT=12415 \
  -v $(pwd)/data/batches:/var/local/images:z \
  uolibraries/rais
```

#### Build Open ONI

Start the development Open ONI container. This will install requirements if needed, and
run various django admin commands as found in [`startup.sh`](startup.sh):

```bash
mkdir -p data/batches data/cache data/bib

docker run -i -t \
  -p 80:80 \
  -e APP_URL=http://site.com:8080 \
  --name openoni-dev \
  --link openoni-dev-mysql:db \
  --link openoni-dev-solr:solr \
  -v $(pwd)/open-oni:/opt/openoni:Z \
  -v $(pwd)/data:/opt/openoni/data:z \
  open-oni:dev
```

In the above example the `open-oni` folder has been host volume mounted for
dynamic development, while the `data` subfolder is coming from the current
directory instead of the app directory. You can mount additional files /
folders as needed. For example, to keep virtualenv files out of your source
tree, you could add this:

```
-v /tmp/CachedENV:/opt/openoni/ENV:Z \
```

The `APP_URL` variable is substituted into the openoni.ini file for RAIS to run
through Apache so you don't have to expose it directly.

Workflow
---

You should be able to develop in the `open-oni` repository folder as normal
i.e. make feature branches etc.  When ready, make a pull request.  To test a
pull request simply pull the remote feature branch (again, as normal) and run
the container including the appropriate volume mount. Using Docker shouldn't
change your regular development workflow much at all.

[`dev.sh`](dev.sh) can be used to stop, rebuild, and restart the dev container in a known
"reset" state.

**Change dependencies**

If requirements.pip is changed, you'll need to run the pip install in the container:

```bash
docker exec -it openoni-dev /pip-install.sh
```

**Load data**

```bash
cd data
wget --recursive --no-host-directories --cut-dirs 1 --reject index.html* --include-directories /data/batches/batch_uuml_thys_ver01/ http://chroniclingamerica.loc.gov/data/batches/batch_uuml_thys_ver01/
cd ..
docker exec -it openoni-dev /load_batch.sh batch_uuml_thys_ver01
```

**Run tests**

```bash
docker exec -it openoni-dev /test.sh
```

**Jump into the container**

```bash
docker exec -it openoni-dev bash
```

**Remove the containers (not persistent data)**

```bash
./docker-clean.sh
```

**Remove persistent data containers and data volumes**
```bash
docker rm openoni-dev-data-mysql openoni-dev-data-solr
docker volume rm $(docker volume ls -qf dangling=true)
```
