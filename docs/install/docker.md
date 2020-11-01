# Docker Installation

- [Note about Windows and Git configuration](#note-about-windows-and-git-configuration)
- [First Time Installation](#first-time-installation)
- [Logs](#logs)
- [Development](#development)
  - [Erase and Start Fresh](#erase-and-start-fresh)
  - [Reviewing Code](#reviewing-code)


If you are already set up with Docker, you may wish to refer to the
[Docker Command Quick Reference](/docs/advanced/docker-reference.md) guide.

## Note about Windows and Git configuration
If you have git setup to use `CRLF` but commit `LF` (this is the default) and you are going to use docker-desktop you will run into
the problem that the start scripts no longer work. You will see error messages like `web_1    | /bin/sh: /entrypoint.sh: /bin/bash^M: bad interpreter: No such file or directory`. To fix, you need to force Git to use `LF` in your working directory by running `git config core.autocrlf false`
This will only affect this repository (add `--global` if you want it to be the default for all your Git repositories).

## First Time Installation
Install Docker using [instructions on Docker's website](https://www.docker.com/products/docker-desktop).

For deploying to a production environment, check out the `main` branch by running
```bash
git clone https://github.com/open-oni/open-oni.git
git checkout main
```

For typical development, clone the `dev` branch by running
```bash
git clone https://github.com/open-oni/open-oni.git
git checkout dev
```

Next you may customize your application by changing the [configuration](/docs/customization/configuration.md#configuring-your-app).
This is completely optional as by default the docker-compose version of Open ONI works without any changes.

Now, boot up the app. Initially, this may take quite some time, but if all goes well in the future it should be fairly rapid:

```bash
docker-compose up
```

If you did not change the default application location, you should be able to see the app running at [localhost](http://localhost).

## Logs

If you only care about watching the web service's apache logs, this may be more
useful: `docker-compose up web`.  And if you want the services to run in the
background without following logs: `docker-compose up -d`.

When services are running in the background, logs are always available via
`docker-compose logs` or `docker-compose logs [service name, such as "web"]`

## Development
This section contains information for those wishing to do development work on Open ONI. 
If you plan to just deploy Open ONI you can stop here and read the remaining documentation in the [Documentation](/docs/README.md) section.

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
