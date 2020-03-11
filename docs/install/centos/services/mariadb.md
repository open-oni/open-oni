# MariaDB

**Contents**

- [Install](#install)
- [Schema and Access Control](#schema-and-access-control)

## Install

General installation and configuration is outside the scope of Open ONI
documentation, but installing the necessary package is the first step:

`sudo yum install mariadb-server`

Django also requires development libraries from MariaDB

`sudo yum install mariadb-devel`


## Schema and Access Control

Create schema `openoni`

Add `openoni` user only connecting from `localhost`

Grant `openoni` user all privileges except `GRANT OPTION`
on `openoni%` schema(s)

`mysql -u root -p`:

```bash
CREATE SCHEMA `openoni`;

USE openoni;

CREATE USER openoni@localhost IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON 'openoni'@'localhost' TO 'openoni'@'localhost';
```
