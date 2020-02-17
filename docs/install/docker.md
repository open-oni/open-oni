# Docker Installation

- [First Time Installation](#first-time-installation)
- [Erase and Start Fresh](#erase-and-start-fresh)
- [Overriding URL and Ports](#overriding-url-and-ports)
- [Reviewing Code](#reviewing-code)
- [Logs](#logs)

## First Time Installation

Install Docker using [instructions on Docker's website](https://www.docker.com/products/docker-desktop).

For typical development, clone the `dev` branch, then copy and modify the

overrides:

```bash
cp docker-compose.override.yml-example docker-compose.override.yml
vim docker-compose.override.yml
```

Now, boot up the app. Initially, this may take quite some time, but if all goes well in the future it should be fairly rapid:

```bash
docker-compose up
```

If you did not change the default application location, you should be able to see the app running at `localhost`.

*You really should read and edit the override - it's mostly there to show what
you **can** do, not necessarily what you **should** do.  The mysql config is
good, but pinning to an old version of RAIS is probably not what you want.*

## Erase and Start Fresh

If you switch branches a lot, or check out the wrong branch, you can have some
super-crazy residual data problems.  As we do development, we change the docker
image configuration, switch out versions of Python libraries, etc.  For a fully
fresh start, do this:

```bash
docker-compose down -v --rmi local
# If you want to truly start fresh, do this instead
# docker-compose down -v --rmi all

# ENV is the Python virtual environment which persists until deleted or
# manually reinstalled
sudo rm ENV/ -rf

# Triple-check your overrides!
vim docker-compose.override.yml
docker-compose up -d
docker-compose logs -f
```

## Overriding URL and ports

If you need to put the app on a custom URL for demoing purposes or something,
you can set the `ONI_BASE_URL` environment variable.  You can also customize the
port with the `HTTPPORT` environment variable, which will be appended if the
value is other than `80`.  When you do this, you have to
make sure you restart the whole stack, as the RAIS container needs to know its
IIIF root URL in order to supply the right values when it's queried for an
image's information.

```bash
docker-compose down
export ONI_BASE_URL=http://192.168.0.5
export HTTPPORT=8080
docker-compose up
```

The above will serve the web app via `http://192.168.0.5:8080`.

Additionally, if you're running a local database and its port conflicts with
the one docker uses, you can change the local port it exposes via the
`RDBMSPORT` environment variable.

## Reviewing Code

To test a pull request, you can often simply run `docker-compose down` followed
by `docker-compose up`.  However, this *may not do what you want*.  In many
cases the code changes are significant enough that you really need to run ONI
"from scratch".  You can do this by destroying all your volumes, your `ENV`
directory, and rebuilding the docker image.

This can be painful to do regularly.  As such, you should consider having a
"clean" ONI checkout instead of testing PRs on your in-development clone:

```bash
git clone https://github.com/open-oni/open-oni.git cleanoni
cd cleanoni
git checkout <branch>
docker-compose build
docker-compose up
```

The `build` step may not seem necessary if you've built the ONI image recently,
but it can be *critical* when testing some PRs.  Sometimes we change packages
at the OS level, and failing to rebuild the image will mean testing against an
obsolete setup!

## Logs

If you only care about watching the web service's apache logs, this may be more
useful: `docker-compose up web`.  And if you want the services to run in the
background without following logs: `docker-compose up -d`.

When services are running in the background, logs are always available via
`docker-compose logs` or `docker-compose logs [service name, such as "web"]`
