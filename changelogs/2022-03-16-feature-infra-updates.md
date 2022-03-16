### Security

### Fixed

### Added

### Changed
- Switch ONI Docker image base to Ubuntu Focal LTS for Python 3.8
  - Change pip-install.sh to install wheel package to prevent bdist_wheel errors
- Docker Compose
  - Switch to use the latest Solr 8.x release
  - Switch to MariaDB 10.6 LTS release
    - Update config to specify `utf8mb3` charset and collation to prevent
      charset collation mismatch error when `utf8(mb3)` charset oddly defaults
      to collation `utf8mb4_general_ci`
    - Remove unused config file variables
- Update Dependency Roadmap

### Removed

### Migration
- If upgrading to MariaDB 10.6.1+, be aware of `utf8` character set default
  changes: https://mariadb.com/kb/en/mariadb-1061-release-notes/#character-sets
  - See documentation for compatible character sets and collations:
    https://mariadb.com/kb/en/supported-character-sets-and-collations/
  - Also see Django recommendations:
    https://docs.djangoproject.com/en/3.2/ref/databases/#creating-your-database
    - TL;DR use `utf8_general_ci` rather than `utf8_unicode_ci` unless you
      require German multi-character comparison to match German DIN-1 ordering

### Deprecated

### Contributors
- techgique
