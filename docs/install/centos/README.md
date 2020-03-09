# Open ONI Docs

This documentation focuses on deployment of Open ONI for production on CentOS 7.

Start with the instructions in this document to download the Open ONI files and
set up the Python environment, then configure the services (
[Apache](/docs/install/centos/services/apache.md),
[MariaDB](/docs/install/centos/services/mariadb.md),
[RAIS](/docs/install/centos/services/rais.md),
[Solr](/docs/install/centos/services/solr.md))
which Open ONI relies upon, and finally configure the [Open ONI Django
App](/docs/install/centos/openoni.md) itself.

**Contents**

Within this document:
- [Open ONI Files](#open-oni-files)
- [Python Environment](#python-environment)

Separate documents:
- [Services](/docs/install/centos/services/)
    - [Apache](/docs/install/centos/services/apache.md)
    - [MariaDB](/docs/install/centos/services/mariadb.md)
    - [RAIS](/docs/install/centos/services/rais.md)
    - [Solr](/docs/install/centos/services/solr.md)
- [Open ONI Django App](/docs/install/centos/openoni.md)

## Open ONI Files
Here is an outline of important default file locations for Open ONI:

```
/opt/openoni/ - Open ONI files
┣━━━ data/batches/ - Newspaper batches
┣━━━ ENV/ - Python 3 virtual environment
┣━━━ onisite/plugins/ - Open ONI plugins
┗━━━ themes/ - Open ONI themes
```

First, download the [latest release of Open
ONI](https://github.com/open-oni/open-oni/releases) and extract the files to
`/opt/openoni/`. This includes config files which will be necessary to configure
our services.

`openoni` is presumed to be a group including all users who will modify ONI
files, ingest batches, etc. Set this group to have write permissions.

```bash
sudo chgrp -R openoni /opt/openoni
sudo find /opt/openoni -type d -exec chmod g+ws {} \;
sudo find /opt/openoni -type f -exec chmod g+w {} \;
```

## Python Environment
Open ONI requires Python 3, so we install it and create a [virtual
environment](https://docs.python.org/3.6/library/venv.html) for Open ONI.

```bash
sudo yum install python3-devel

cd /opt/openoni/
python3 -m venv ENV
source ENV/bin/activate

# Update pip and setuptools
pip install -U pip
pip install -U setuptools
```
