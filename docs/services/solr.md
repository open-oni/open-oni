# Solr 6.x

**Contents**

- [Install](#install)
- [Create Open ONI Core](#create-openoni-core)
- [Backups](#backups)
- [Configure](#configure)


## Install

Installation and configuration documentation in progress


## Create Open ONI Core
```bash
sudo -u solr /opt/solr/bin/solr create_core -c openoni
```


## Backups
Backup scripts in progress

Download the files to `/var/local/solr/`

Follow the instructions in the accompanying README.md file

Schedule a regular backup in `/etc/crontab`:
```cron
# REGULAR TASKS

# Daily Solr Backup at 4am
  0  4  *  *  * solr       /var/local/solr/backup/backup.py -q
```


## Configure
Further config is handled after the Open ONI repository is cloned

[Configure Open ONI Schema](/docs/openoni.md#solr-schema)

