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

- [Georgia Historic Newspapers](https://gahistoricnewspapers.galileo.usg.edu/)
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
for the Humanities grant](https://library.uoregon.edu/node/7671) to develop
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
Python | 3.12 | 2028-10 | 3.14 | https://www.python.org/downloads/
Django | 5.2 LTS | 2028-04 | 6.2 LTS, 2027-04 | https://www.djangoproject.com/download/#supported-versions
MariaDB | 11.4 | 2029-05-29 | Next LTS in ~2 years | https://mariadb.org/about/#maintenance-policy
Solr | 10.x | Approx 2029, based on past major release dates | TBD | https://lucene.apache.org/solr/downloads.html#about-versions-and-support
RAIS | 4.x | Unknown | TBD | https://github.com/uoregon-libraries/rais-image-server
jQuery | 3.7.1 | Unknown | TBD | https://github.com/jquery/jquery/wiki/Roadmap
Bootstrap | 3.4.1 | 2019-07-24 | Upgrade as part of NEH grant | https://github.com/twbs/release
OpenSeadragon | 6.0.2 | Unknown | 7.x | https://github.com/openseadragon/openseadragon
tablesorter | 2.31.3 | Unknown | TBD | https://github.com/Mottie/tablesorter/wiki/Changes

Note: [jQuery cannot be updated to 4.x until Bootstrap is updated to 5.x, where
it is optional](https://getbootstrap.com/docs/5.3/getting-started/javascript/#optionally-using-jquery).
Migration to Bootstrap 5.x has been done on the [`dev-2.0`
branch.](https://github.com/open-oni/open-oni/tree/dev-2.0)

Also see our [Python package
dependencies](https://github.com/open-oni/open-oni/blob/dev/requirements.txt).
We've only added constraints where we are confident they are necessary to avoid
breaking changes from new releases.

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
Discord](https://discord.gg/AmSyaRRSJY).
These guidelines are intended both to keep conversation in the open where it may
benefit all of the Open ONI community and to protect developers' already limited
time.

## Contact Us
We prefer to communicate on the [Open ONI
Discord](https://discord.gg/AmSyaRRSJY),
but if you have trouble or prefer not to use Discord, email Greg Tunink (techgique
[at] unl.edu).

### Security
To report a security concern or vulnerability, please ask for a project
maintainer to direct message you on the [Open ONI
Discord](https://discord.gg/AmSyaRRSJY)
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
[Licensed](https://github.com/open-oni/open-oni/blob/dev/LICENSE) under the
Apache License, Version 2.0
