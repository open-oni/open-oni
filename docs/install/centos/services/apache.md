# Apache

**Contents**

- [Install](#install)
    - [SELinux Permissions](#selinux-permissions)
    - [mod_wsgi](#mod_wsgi)
- [Configure](#configure)
    - [mod_wsgi Run Directory](#mod_wsgi-run-directory)
    - [Virtual Host Config](#virtual-host-config)

## Install

General installation and configuration is outside the scope of Open ONI
documentation, but installing the necessary packages is the first step:

`yum install httpd httpd-devel mod_ssl policycoreutils-python`

### SELinux Permissions
SELinux requires Open ONI's file have appropriate file contexts for Apache
(httpd) to access them.

```bash
# General files need Apache-readable context
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/openoni(/.*)?"

# Python libraries need Apache-executable context
sudo semanage fcontext -a -t httpd_sys_script_exec_t "/opt/openoni/ENV/lib/python3.6/site-packages/.+\.so"

# Static asset compilation path needs Apache-writable context
mkdir /opt/openoni/static/compiled
sudo semanage fcontext -a -t httpd_sys_rw_content_t "/opt/openoni/static/compiled(/.*)?"

sudo restorecon -F -R /opt/openoni/
```

### mod_wsgi
The Django app will be deployed with Apache via mod_wsgi, but a Python
3-compatible version must be installed via pip, rather than the Python 2 version
available in the yum repositories. This install depends upon the `gcc` and
`httpd-devel` packages.

```bash
sudo yum install gcc httpd-devel

cd /opt/openoni/
source ENV/bin/activate
pip install mod_wsgi

# Set appropriate SELinux contexts on new mod_wsgi files
sudo restorecon -F -R /opt/openoni/ENV/

# Output the Apache config directives to load Python 3 mod_wsgi
mod_wsgi-express module-config
```

Add the directives to your Apache server-wide configuration, because they are
not allowed inside `<VirtualHost>` blocks. Unless you have a custom
configuration file organization, this should be either
`/etc/httpd/conf/httpd.conf` or you may separate the directives into their own
drop-in file in `etc/httpd/conf.d/`, e.g. `mod_wsgi_openoni_py36.conf`.

They should resemble:
```ini
LoadModule wsgi_module "/opt/openoni/ENV/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
WSGIPythonHome "/opt/openoni/ENV"
```

mod_wsgi also needs this directive applied server-wide:

```ini
WSGISocketPrefix /var/run/mod_wsgi/
```

## Configure

### mod_wsgi Run Directory
Manually create initially:<br>
`mkdir /run/mod_wsgi`

Create automatically at boot going forward

`vim /etc/tmpfiles.d/mod_wsgi.conf`:
```ini
d /run/mod_wsgi 755 root root
```

### Virtual Host Config
Copy [Django Apache config](/conf/apache/django.conf) into an appropriate
drop-in directory which will be included in your virtual host:

```bash
cp /opt/openoni/conf/apache/django.conf /etc/httpd/(path/to/vhost/drop-in-dir)/
```

Or copy the contents into your virtual host file.
