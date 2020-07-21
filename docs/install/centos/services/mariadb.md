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
`mysql -u root -p`:

```bash
-- Create the database and switch to use it
CREATE SCHEMA `openoni`;
USE openoni;

-- Add a user which can only connect locally
CREATE USER 'openoni'@localhost IDENTIFIED BY '(passphrase)';

-- Grant necessary privileges
GRANT ALL PRIVILEGES ON `openoni`.* TO 'openoni'@'localhost';
```
