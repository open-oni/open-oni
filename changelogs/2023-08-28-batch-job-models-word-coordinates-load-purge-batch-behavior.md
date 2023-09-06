### Fixed

- No longer print multiple exceptions when trying to purge a batch that doesn't exist

### Added

- `completed_at` field for Batch model to record batch_load completion
  - Test which required use of patching timezone.now()
- Job model with UUID, last_modified, and enums for JobType and Status values
  - Integrated into batch load and purge
    - If a job is already in progress for a batch, others are denied
    - Only allow one type of batch command per batch at a time
  - Tests to verify logic working as intended
    - Include comments to help keep track of fake records
      and having the same timestamp for all last_modified values

### Changed

- Docker startup script now creates `/data/word_coordinates/` directory and
  sets ownership by Apache so Django can modify files during load/purge via
  web request rather than command line (e.g. admin API plugin)
  - Also documented for CentOS deployments
- Revised exception and error handling in load and purge batch code
  - Avoid exceptions printed to terminal for handled situations
  - Revise messages for clarity and include path to the corresponding log file
- Add interactive arg to load and purge batch management commands
  - Raise exceptions for commands called non-interactively so context calling
    can handle messages and return appropriate responses to requests

### Migration

For CentOS deployments, update word_coordinates permissions:
```bash
sudo chown apache:openoni /opt/openoni/data/word_coordinates
sudo chmod 2775 /opt/openoni/data/word_coordinates
sudo semanage fcontext -a -t httpd_sys_rw_content_t "/opt/openoni/data/word_coordinates(/.*)?"

sudo restorecon -F -R /opt/openoni/
```

### Contributors

- Greg Tunink (techgique)
