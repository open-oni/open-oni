### Changed

- Complete refactor of the container side of ONI
  - The stack now works with `podman` and `podman compose`
  - Apache has been replaced with Caddy to more easily separate app and web
    server concerns
  - All direct filesystem mounts are removed and *strongly* discouraged in the
    example files and documentation
  - Compose environment settings are simpler and smarter, e.g., a single
    `DB_PASSWORD` environment variable will set up ONI and MariaDB.
  - Customization of ONI is significantly easier. Mostly.
    - All basic settings are done in `.env`
    - `settings_local.py` can now be largely ignored after setting up plugins
      and themes
    - The only time you'll edit the compose override is to change the stack
      behavior (e.g., how volumes are created / mounted).
  - Generally speaking we're now closer to a production-friendly compose stack
  - *You will need to spend more time understanding the stack and compose in
    general, as we're relying on more advanced features than before.*
- UTF8 migration is always skipped for sqlite, regardless of the settings
  module's name

### Migration

- Archive your current dev environment. Read the docker install guide
  carefully, read the compose override example carefully, read `.env.example`
  carefully. Reapply your settings one at a time.

### Contributors

- Jeremy Echols
