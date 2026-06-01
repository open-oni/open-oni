# Bot Protection

To help prevent resource problems caused by heavy / aggressive bot crawling,
Open ONI's compose setup includes optional support for putting a challenge
proxy in front of whatever paths you choose. Examples for two proxies are
included:

- **TPS** (the [Turnstile Proxy Server][tps]) sits in front of ONI to present a
  Cloudflare Turnstile challenge closer to the edge than if you embedded
  Turnstile directly into your pages. This requires a Cloudflare account, but
  it is very effective at stopping bots.
- **Anubis** ([techaro/anubis][anubis]) also sits in front of ONI to present a
  proof-of-work challenge. Anubis is fully self-hosted, but it only raises a
  scraper's cost rather than trying to verify a client is human.

[tps]: https://github.com/uoregon-libraries/turnstile-proxy-server
[anubis]: https://anubis.techaro.lol/

## Common Setup

We chose to separate the "protected path" configuration from the service that
does the protecting. This should make it easy to use TPS or Anubis (or some
other option we haven't even considered) in a very similar way.

If you choose to enable either service, you follow roughly the same steps:

1. Include one of the bot protection services' compose files in your stack
2. Set up service-specific configuration / files
3. Copy the common "server" snippet,
   `docker/caddy/examples/bot-protection.server.caddyfile`, into the Caddy
   configuration volume, `caddy-conf`
4. Copy a service-specific "site" snippet
   (`docker/caddy/examples/bot-protection-*.site.caddyfile`) into the Caddy
   configuration volume, and edit as needed to alter protected URLs

### Include a bot-protection service

Uncomment the `include` of your choice in the compose override. e.g.:

```yaml
include:
  - tps.compose.yaml
```

### Set up service-specific configuration / files: TPS

To use TPS, you need to have a Cloudflare account. Create a Turnstile widget in
your Cloudflare dashboard to get a site key and secret key. For local testing,
use Cloudflare's [test keys][test-keys].

Review the environment settings in `.env.example` (prefixed with `TPS_`).

[test-keys]: https://developers.cloudflare.com/turnstile/troubleshooting/testing/

### Set up service-specific configuration / files: Anubis

You'll need to get a bot-policy file in the `anubis-policies` mount.
`docker/caddy/examples/anubis-botPolicies.yaml` is a good default, though you
can edit this if you want more advanced rules.

Note that the Anubis volume is read-only. If you haven't already, look at
["Copying files into read-only volumes"][docker-copy-ro] in our docker
installation guide.

[docker-copy-ro]: /docs/install/docker.md#copying-files-into-read-only-volumes

## Caddy Configuration In Detail

A full explanation of the various tools Caddy offers is out of scope, but a few
notes on basic ONI bot protection are included below.

### Configuration files

As mentioned above, all setups require a server file that defines an internal
listener, and a service-specific "site" file. Look at the examples in
`docker/caddy/examples`. For most simple setups, these can be used as-is.

The destination filenames can be whatever you want as long as the internal
listener uses the `.server.caddyfile` suffix, and the routing uses the
`.site.caddyfile` suffix.

Copy these as-is, or edit them and then copy them, into the `caddy-conf`
volume.

Note that the Caddy volumes are read-only. If you haven't already, look at
["Copying files into read-only volumes"][docker-copy-ro] in our docker
installation guide.

### Choosing which paths are protected

Edit the `@protected` matcher in your service-specific `*.site.caddyfile`. It
is a normal [Caddy path matcher][path-matcher], and the only difference between
TPS and Anubis is that Anubis requires `/.within.website/*` to be explicitly in
this list.

Simply add or remove entries in the `path` list to change what is challenged.

[path-matcher]: https://caddyserver.com/docs/caddyfile/matchers#path

### Allowing trusted IP ranges

To exempt known-good networks (a campus range, a monitoring service) for either
proxy, add a `not client_ip` clause to the `@protected` matcher:

```caddyfile
@protected {
  path /data/* /search/*
  not client_ip 203.0.113.0/24 198.51.100.10
}
```

If ONI sits behind another reverse proxy or a CDN, Caddy sees that hop's IP
unless you tell it whom to trust. Configure [`trusted_proxies`][trusted] and
`client_ip_headers` in a global options snippet.

[trusted]: https://caddyserver.com/docs/caddyfile/options#trusted-proxies
