# Open ONI
**Open Online Newspaper Initiative (Open ONI)** is a community-maintained
project to make historic American newspapers browsable and searchable on the
web. We aim to enable individual state and library-based newspaper collections
to more easily provide these core capabilities, as well as develop new common
features and improvements.

Read our [About Open ONI web page](https://open-oni.github.io/about/) for more
information about the project's origins and history.

## Open ONI-powered Sites
Visit sites currently powered by Open ONI:

- [Historic Oregon Newspapers](https://oregonnews.uoregon.edu/)
- [Pennsylvania Newspaper Archive](http://panewsarchive.psu.edu/)
- [Nebraska Newspapers](https://nebnewspapers.unl.edu/)

View ["Sites using Open ONI" in our
wiki](https://github.com/open-oni/open-oni/wiki/Sites-Using-Open-ONI) for links
to the sites' source code.

## Install
To evaluate the software, we recommend installing from the [latest Open ONI
release](https://github.com/open-oni/open-oni/releases).

The 1.0 release includes upgrading Django to the latest LTS 2.2 release along
with migrating to Python 3 and upgrading Solr and MariaDB to more recent
releases. Note that release 0.11 and prior run Python 2 and Django 1.11 LTS
which goes out of support in April 2020.

If you're interested in more recent changes, check out the `dev` branch.

### Resource Requirements

This is a ballpark estimate of resources we recommend for running Open ONI in
production. Open ONI is quite capable with minimal processing and memory
resources.

CPU | Memory | Storage (with TIFFs) | Storage (JP2s only)
----|--------|----------------------|--------------------
Modern CPU with two (virtual) cores | 6GB | 1TB per ~25K pages| 1TB per ~100K pages

We share more information on the [Resource
Usage](https://github.com/open-oni/open-oni/wiki/Resource-Usage) page in our
wiki, which may further inform your resource allocation.

### Dependency Roadmap

We expect Open ONI's major components (aside from Bootstrap 3) to be supported
until the next Django LTS release 3.2 in April 2021, at which point we will
likely upgrade Open ONI's components between major releases again.

Component | Version | Supported Until | Next Target Release | Documentation
----------|---------|-----------------|---------------------|--------------
Python | 3.6 | 2021-12 | TBD | https://www.python.org/dev/peps/pep-0494/#lifespan
Django | 2.2 LTS | 2022-04 | 3.2 LTS, 2021-04 | https://www.djangoproject.com/download/#supported-versions
MariaDB | 10.4 | 2024-06 | TBD | https://mariadb.com/kb/en/mariadb-server/
Solr | 8.x | Approx 2022, based on ~18mo major release cycle | TBD | https://lucene.apache.org/solr/downloads.html#about-versions-and-support
jQuery | 3.4.1 | Unknown | TBD | https://github.com/jquery/jquery/wiki/Roadmap
Bootstrap | 3.4.1 | 2019-07-24 | TBD | https://github.com/twbs/release
OpenSeadragon | 2.4.1 | Unknown | TBD | https://github.com/openseadragon/openseadragon
tablesorter | 2.31.2 | Unknown | TBD | https://github.com/mottie/tablesorter/

## Documentation
- [Installation, Configuration, and
  Troubleshooting](https://github.com/open-oni/open-oni/tree/dev/docs)
  - [Wiki - Additional Deployment Info](https://github.com/open-oni/open-oni/wiki)
- [Changelog](https://github.com/open-oni/open-oni/tree/dev/CHANGELOG.md)
- [Contribute](https://github.com/open-oni/open-oni/tree/dev/CONTRIBUTING.md)
- [About Open ONI, Project History](https://open-oni.github.io/)

## Support
Note that maintainers can only provide a minimal amount of assistance while
working on Open ONI part-time. Developers cannot be expected to provide
extensive one-on-one support.

We are glad to provide support specifically related to Open ONI, but anyone
wanting to work with Open ONI should begin with some foundational knowledge of
Linux, Docker, Apache, Python, Django, Solr, MariaDB/MySQL, and IIIF. There are
other resources and communities better suited to aid in getting started and
familiar with those technologies, so general assistance with them falls outside
the scope of what to expect Open ONI developers to provide.

We ask that bugs and feature requests be submitted to [Open ONI on
GitHub](https://github.com/open-oni/open-oni/issues). Please confine other
questions and conversation about Open ONI development and use to [Open ONI's
Slack](https://join.slack.com/t/open-oni/shared_invite/enQtMzg5MDg5NjU5MDU2LTA4MmViOTkxZDliZWZmM2FlMGU5ODZjNDU0OWQxYzIzMTY1YmFlMWEzZDFkNDNjZmYxYzUyMmMwZjlkMjU1MGE).
These guidelines are intended both to keep conversation in the open where it may
benefit all of the Open ONI community and to protect developers' already limited
time.

## Contact Us
We prefer to communicate on the [Open ONI
Slack](https://join.slack.com/t/open-oni/shared_invite/enQtMzg5MDg5NjU5MDU2LTA4MmViOTkxZDliZWZmM2FlMGU5ODZjNDU0OWQxYzIzMTY1YmFlMWEzZDFkNDNjZmYxYzUyMmMwZjlkMjU1MGE),
but if you have trouble or prefer not to use Slack, email Greg Tunink (techgique
[at] unl.edu).

### Security
To report a security concern or vulnerability, please ask for a project
maintainer to direct message you on the [Open ONI
Slack](https://join.slack.com/t/open-oni/shared_invite/enQtMzg5MDg5NjU5MDU2LTA4MmViOTkxZDliZWZmM2FlMGU5ODZjNDU0OWQxYzIzMTY1YmFlMWEzZDFkNDNjZmYxYzUyMmMwZjlkMjU1MGE)
or email Greg Tunink (techgique [at] unl.edu). Maintainers will evaluate,
discuss responsible disclosure and patching, and give many thanks and credit for
your generous assistance.

## Contribute
If you are interested in collaborating on the project, please review
[CONTRIBUTING.md](https://github.com/open-oni/open-oni/tree/dev/CONTRIBUTING.md)
for more details. Everyone interacting within the Open ONI community is expected
to follow the [Open ONI Community Code of
Conduct](https://github.com/open-oni/open-oni/tree/dev/CODE_OF_CONDUCT.md)

## License
[Licensed](https://github.com/open-oni/open-oni/blob/main/LICENSE) under the
Apache License, Version 2.0
