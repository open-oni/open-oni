### Added

- Optional bot protection: you can now put a challenge proxy in front of
  expensive paths (examples for using TPS and Anubis are included)

### Changed

- Caddy now loads custom config from the `caddy-conf` volume by file suffix:
  - `*.site.caddyfile` is imported into the `:80` site (before the default
    routing, so a copied-in rule wins)
  - `*.server.caddyfile` is imported at the top level (for extra listeners like
    the bot-protection backend)

### Migration

- The sitemap example moved and was renamed to
  `docker/caddy/examples/sitemap.site.caddyfile`. If you had copied the old
  `sitemap.Caddyfile` into `caddy-conf`, re-copy it under a name ending in
  `.site.caddyfile` so Caddy imports it
- If you had Caddy rules in the `caddy-conf` volume, you'll need to rename them
  to `*.site.caddyfile` so they're included as site rules

### Contributors

- Jeremy Echols
