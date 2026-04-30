# Docker Installation And Usage

Note that these instructions generally work just fine with either of the podman
or docker container engines.

You will need to be familiar with whichever tool you choose, as container
setups can be confusing and easily cause hard-to-debug problems otherwise.

## Setup

You'll need to clone the ONI source. For demos or production setups you should
always use the "main" branch. Development usually starts with the "dev" branch;
see our ["Contributing to Open ONI"](/CONTRIBUTING.md) document for
contributor-specific information.

You'll want to build the stack before anything else so the initial startup
isn't too slow, e.g., `docker compose build`.

Next, you'll want to copy the example compose override:

```bash
cp compose.override.example.yaml compose.override.yaml
```

*Read it thoroughly*, and edit as needed. Generally for development or quick
demos, you can use this with minimal modifications. For anything remotely
production-related, you *must* make some adjustments.

### Environment

Now copy the environment example:

```bash
cp .env.example .env
```

Again, *read it thoroughly* and modify settings as needed for your setup.

### Volumes

The compose override example shows how to use the project's `data` directory as
the `oni-data` volume as well as mounting some subdirectories for development.

Some examples can be used as-is, but again, please read carefully. e.g., in dev
it's almost always fine to reconfigure the `oni-data` volume mount, or even to
mount some local directories right into running containers. In production,
`oni-data` may need a completely different configuration, and mounting the
project's directories is rarely a good idea.

A lot of the time, you don't need to mount anything at all. You can use `docker
cp`, for instance, to alter your configuration, copy plugins into a volume,
etc. "One and done" changes may not warrant exposing an entire volume forever.

So we advise that you let podman manage volumes when possible. You will rarely
need to change plugins, themes, or even configuration. This is especially true
in production environments.

---

Remember: volume definitions are an "on-create" mechanic. Once a volume is
created, the driver and options are ignored when restarting the stack. You must
destroy volumes (e.g., `podman compose down -v`, `docker volume rm`, etc.) in
order to get the container engine to re-read the new definition.

Removing a volume removes whatever the engine created. For volumes with no
custom driver options, the engine *creates the directory*. In these cases,
removing the volume **also removes the data**.

#### `oni-config`

This is a special volume that behaves a bit differently because we wanted a way
to isolate configuration in a manner Django doesn't allow by default.

On first run, this volume will get copies of the two configuration files users
may have to edit: `onisite/urls.py` and `onisite/settings_local.py`. You
shouldn't need to customize these files beyond adding themes and plugins to
`INSTALLED_APPS`, and possibly modifying `urls.py` to expose a plugin's
path(s). In particular, if a setting can be provided by the environment, you
are *strongly encouraged* to use the environment, not edit the settings file
directly.

You can use the `oni-data` compose override example to expose `oni-config` if
necessary, but as mentioned above, this is generally not necessary, and
long-term not a good idea.

### Configuration architecture

Generally your compose concerns will live in `compose.override.yaml`,
per-environment settings are in `.env`, and plugin/theme settings have to be
manually placed in the `oni-config` volume.

We've attempted to get configuration into the environment as much as we can,
but the `oni-config` volume is a bit tricky for users of custom themes and
plugins. Since most users will want to have their own theme, at a minimum
you're likely to need to change the `INSTALLED_APPS` setting in
`settings_local.py`.

Because of the variations that can exist in different setups, especially when
there are complex plugins and themes, you might find that despite our advice
you need to mount a lot more of the project into running containers even in
production. *This is okay!* It's a bad idea if you are new to devops, but if
you understand the risks and you test things very carefully, advanced use-cases
can work this way. Just make sure you know the risks you can run into.

## Management

Management commands in a container setup are largely the same as they are on a
normal VM, with just a few key exceptions:

- The "app" service uses the Python image, so you have to execute commands in a
  running instance of "app".
- "app" doesn't use a virtual environment, as it's a single-purpose service. No
  need for `source ENV/bin/activate`.
- The "app" image's working directory is `/opt/openoni`, so you don't have to
  change directory.
- Running containers store data in `/var/local/oni-data`. This means batches
  will be visible to running containers in `/var/local/oni-data/batches`.

Putting this all together, management commands will always look like this:

```bash
docker compose exec app ./manage.py <command> <args>
```

...and here's how you might load a batch[^batch-volume]:

```bash
docker compose exec app ./manage.py load_batch /var/local/oni-data/batches/batch_foo_xyzzy_ver01
```

You can otherwise follow the normal [instructions for admin
commands](/docs/advanced/admin-commands.md).

[^batch-volume]: You must put batches in the `oni-data` volume's "batches"
    subdirectory in order to load them. You'll need to either use `docker cp`
    or configure the volume to use storage you can copy batches into directly
    (the compose override example shows one way this could be achieved).

## Development

This section contains information for those wishing to do development work on
Open ONI. If you plan to just deploy Open ONI you can stop here and read the
remaining documentation in the [Documentation](/docs/README.md) section.

### Rebuilding

Because of the production-centric approach we're trying to take with the
container setup, making changes to any of ONI's files will usually require
taking down the "app" service, rebuilding it, and starting it up again.

If this is too cumbersome, there are ways around it depending on your tech
stack. All compose users can mount host directories into the running
containers, though you should do so carefully to avoid permissions issues
(e.g., only mount "core").

Docker compose also supports the [develop specification][compose-develop], but
unfortunately, at the moment (April 2026), podman compose does *not* support
it, and doesn't seem likely to anytime soon. (See ["`watch` support" on podman's
github issue tracker][podman-watch-issue])

[compose-develop]: <https://docs.docker.com/reference/compose-file/develop/>
[podman-watch-issue]: <https://github.com/containers/podman-compose/issues/792>

We haven't tested this, so *use at your own risk*, but an example of using
`develop` might look like this in your compose override:

```yaml
services:
  app:
    develop:
      watch:
        - action: sync+restart
          path: ./core
          target: /opt/openoni/core
        - action: sync+restart
          path: ./onisite
          target: /opt/openoni/onisite
        - action: sync+restart
          path: ./themes
          target: /opt/openoni/themes
```

### A Note On Mounting Local Directories

If you absolutely need to get live-reloads, or make it easier to copy themes
and plugins, it is strongly recommended that you only use local bind mounts for
specific subdirectories. *Mounting "." is a very bad idea 99% of the time!*

Mounting any local directories will complicate permissions, especially in a
rootless setup, but mounting the full app is extra tricky the way our stack is
set up: static files are in a volume under the project root, so if you mount
the project root in, you're nesting volumes; configuration files are handled
via symlinking, so you'll end up with local files that link to nowhere; etc.

Also note that if you mount things from your host, "web" and "app" will need
different directories mounted in different ways. "web" needs batches and word
coordinates, for instance, but not ONI config files.

Consider only mounting individual subdirectories as needed, and only things you
intend to change immediately.

*The one exception is when upgrading pip dependencies, where you need to change
requirements files and get them in the git repo. We advise taking the safe
(though slow) route of copying files in and out of the container, and still
avoiding mounting the project root.*

### Erase and Start Fresh

If you switch branches a lot, or check out the wrong branch, you can have some
residual data problems. As we do development, we change the docker image
configuration, switch out versions of Python libraries, etc. For a fully fresh
start, you can remove all ONI images and volumes. Be aware that volumes you
control (e.g. with custom `driver_opts` settings) will only have their
definitions recreated, *not* their data.

```bash
docker compose down -v --rmi local
docker compose up -d
docker compose logs -f web app
```

### Reviewing Code

To test others' code, usually you just stop services, check out a branch,
rebuild images, and start up docker compose again. Sometimes this doesn't do
what you want, however, and you have to destroy all volumes, and even manually
clear out custom volumes' data.

This can be painful to do regularly. As such, you should consider having a
"clean" ONI checkout just for code review, with settings that are as close to
the defaults as possible, with one exception: `COMPOSE_PROJECT_NAME` *must* be
different from what you use in your main project! If two projects share the
same compose project name, wackiness will ensue, and not the good kind.
