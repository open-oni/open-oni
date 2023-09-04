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
- [Nebraska Newspapers](https://nebnewspapers.unl.edu/)
- [North Carolina Newspapers](https://www.digitalnc.org/collections/newspapers/)
- [Pennsylvania Newspaper Archive](https://panewsarchive.psu.edu/)

View ["Sites using Open ONI" in our
wiki](https://github.com/open-oni/open-oni/wiki/Sites-Using-Open-ONI) for links
to the sites' source code.

## Install
Open ONI requires newspaper data in specific files and formats which comprise a
"batch". We provide [small sample
batches](https://github.com/open-oni/sample-data) for testing and [documentation
on how to create a
batch](https://github.com/open-oni/open-oni/wiki/Create-Your-Own-Batch). The
Library of Congress also provides [Chronicling America newspapers as
batches](https://chroniclingamerica.loc.gov/batches/).

Open ONI does not currently provide tools to create batches, but the [University
of Oregon and University of Nebraska-Lincoln were awarded a National Endowment
for the Humanities grant](https://web.archive.org/web/20230101212540/https://library.uoregon.edu/node/7671) to develop
software and features to assist with batch creation, enable issue editing, and
update the Open ONI front end framework alongside an accessibility / user
experience audit.

To evaluate the software, we recommend downloading the [latest Open ONI
release](https://github.com/open-oni/open-oni/releases) and following [installation documentation](https://github.com/open-oni/open-oni/tree/main/docs#installation-and-updating). If you're interested in more recent changes, check out the `dev` branch.

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

Component | Version | Supported Until | Next Target Release | Documentation
----------|---------|-----------------|---------------------|--------------
Python | 3.8 | 2024-10 | 3.10 | https://peps.python.org/pep-0569/#lifespan
Django | 3.2 LTS | 2024-04 | 4.2 LTS, 2023-04 | https://www.djangoproject.com/download/#supported-versions
MariaDB | 10.6 | 2026-07-06 | Next LTS in ~2 years | https://mariadb.org/about/#maintenance-policy
Solr | 8.x | Approx 2022, based on ~18mo major release cycle | TBD | https://lucene.apache.org/solr/downloads.html#about-versions-and-support
RAIS | 4.x | Unknown | TBD | https://github.com/uoregon-libraries/rais-image-server
jQuery | 3.6.0 | Unknown | TBD | https://github.com/jquery/jquery/wiki/Roadmap
Bootstrap | 3.4.1 | 2019-07-24 | Upgrade as part of NEH grant | https://github.com/twbs/release
OpenSeadragon | 2.4.2 | Unknown | 3.x | https://github.com/openseadragon/openseadragon
tablesorter | 2.31.3 | Unknown | TBD | https://github.com/Mottie/tablesorter/wiki/Changes

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
