# Apache

**Contents**

- [Install](#install)
- [Extra Dependencies](#extra-dependencies)
- [Configure](#configure)
    - [Directory Indices](#directory-indices)
    - [mod_wsgi Run Directory](#mod_wsgi-run-directory)
    - [Python Randomized Hashing](#python-randomized-hashing)
    - [Virtual Host Config](#virtual-host-config)


## Install

Installation and configuration documentation in progress


## Extra Dependencies
`yum install mod_wsgi`


## Configure

### Directory Indices
Open ONI uses directory indices to allow visitors to browse data files

We generally disable directory indices and the icons the Apache-generated pages
use, so we need to re-enable access to the icons

`vim /etc/httpd/conf.d/autoindex.conf`:
```
Alias /icons/ "/usr/share/httpd/icons/"
```

### mod_wsgi Run Directory
Manually create initially:<br>
`mkdir /run/mod_wsgi`

Create automatically at boot going forward

`vim /etc/tmpfiles.d/mod_wsgi.conf`:
```ini
d /run/mod_wsgi 755 root root
```

### Python Randomized Hashing
[Denial-of-Service Protection](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/#python-options)

`vim /etc/systemd/service/httpd.service`:
```ini
.include /lib/systemd/system/httpd.service
[Service]
Environment=PYTHONHASHSEED=random
```

`sudo systemctl restart httpd`

### Virtual Host Config
Copy [Django Apache config](/conf/apache/django.conf) into an appropriate
drop-in directory which will be included in your virtual host or copy the
contents into your virtual host file

```bash
cp /opt/openoni/conf/apache/django.conf /etc/httpd/local/vhosts/_vhost-includes/
```

