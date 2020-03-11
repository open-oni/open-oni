# Solr

**Contents**

- [Dependencies](#dependencies)
- [Install](#install)
- [Configure](#configure)

## Dependencies
- Download the [Open ONI files](/docs/install/centos/README.md#open-oni-files)
- Prepare the [Python environment](/docs/install/centos/README.md#python-environment)

## Install

General installation and configuration is outside the scope of Open ONI
documentation, but follow these to start:
- [Solr Downloads](https://lucene.apache.org/solr/downloads.html)
- [Production Service
  Install](https://lucene.apache.org/solr/guide/8_3/taking-solr-to-production.html)

## Configure
```bash
cd /opt/openoni/
source ENV/bin/activate
./manage.py setup_index
```
