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

## Routing

Routing *is confusing* when you look at bot protection! This can make debugging
tough, especially when doing development or testing.

The players:

- **Client**: usually (hopefully), a real user making a request via a web
  browser, but a client can be anything accessing your site
- **Caddy-Ext**: the Caddy listener exposed directly to the Internet
- **Caddy-Int**: the Caddy listener that's only accessible from within the
  docker / podman network
- **Challenger**: the TPS or Anubis service the intercepts protected URLs
- **App**: The server runs gunicorn, which serves ONI pages

The challenge loop:

1. **Client** makes a request for an ONI page
2. **Caddy-Ext** is always the first responder for any request
   - If the requested URL is in the `@protected` list, **Caddy-Ext**
     reverse-proxies to **Challenger**
   - Otherwise, **Caddy-Ext** either serves it directly (static assets) or
     dispatches to **App**
     - *The flow is complete*
3. **Challenger** checks **Client** data
   - If **Client** has a valid challenge token, we break out of the loop
     immediately
   - Otherwise, **Challenger** sends the challenge HTML / JS back to **Client**
4. **Client** solves the challenge, usually non-interactively, and stores the
   solved challenge in a special token
   - Most basic bots, and some advanced bots, are stopped here, unable to run
     the challenge (e.g., inability to run JS, lack of resources to solve the
     challenge, blocked by other challenger rules, etc.)
5. **Client** sends a new request with the token
   - *This repeats the flow from step 2*

Once step 3's "break out of the loop" occurs:

6. **Caddy-Int** receives the request and uses the same rules **Caddy-Ext**
   uses on unprotected paths (serving static assets or dispatching to **App**)
   - There is no challenge logic on **Caddy-Int** because it is unreachable
     externally (it only receives verified post-challenge requests)
   - *The flow is complete*

Note that in some cases, the challenge token will become invalidated. Things
like switching IP addresses can be a flag that a challenge needs to be issued
again, as the more aggressive bots rotate IP addresses for every request.

## Common Setup

We chose to separate the "protected path" configuration from the service that
does the protecting. Both services register the network alias `challenger`,
which is what the Caddy snippets proxy to, so the same Caddy configuration
works for TPS or Anubis (or some other option we haven't even considered) -
the only choice you make is which compose file to include.

If you choose to enable either service, you follow roughly the same steps:

1. Include one (and only one) of the bot protection services' compose files in
   your stack
2. Set up service-specific configuration / files
3. Copy the "server" snippet,
   `docker/caddy/examples/bot-protection.server.caddyfile`, into the Caddy
   configuration volume, `caddy-conf`
4. Copy the "site" snippet,
   `docker/caddy/examples/bot-protection.site.caddyfile`, into the Caddy
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
listener, and a "site" file that defines the protected paths. Both are shared
by TPS and Anubis. Look at the examples in `docker/caddy/examples`. For most
simple setups, these can be used as-is.

The destination filenames can be whatever you want as long as the internal
listener uses the `.server.caddyfile` suffix, and the routing uses the
`.site.caddyfile` suffix.

Copy these as-is, or edit them and then copy them, into the `caddy-conf`
volume.

Note that the Caddy volumes are read-only. If you haven't already, look at
["Copying files into read-only volumes"][docker-copy-ro] in our docker
installation guide.

### Choosing which paths are protected

Edit the `@protected` matcher in your `*.site.caddyfile`. All protected paths
live in a single [Caddy `path_regexp` matcher][path-regexp-matcher], with each
protected prefix being one alternative in the regex's group. Add or remove
alternatives to change what is challenged.

One entry deserves a special mention: `/.within.website/` is where Anubis
serves its challenge assets, so it must route to the challenger for Anubis to
work. TPS never uses the path, and ONI has no dot-prefixed routes, so leaving
it in place under TPS is harmless.

[path-regexp-matcher]: https://caddyserver.com/docs/caddyfile/matchers#path_regexp

### Allowing trusted IP ranges

To exempt known-good networks (a campus range, a monitoring service) for either
proxy, add a `not client_ip` clause to the `@protected` matcher, e.g.,

```caddyfile
@protected {
  path_regexp ^/(data/|search/|issues/|lccn/\w+/issues/first_pages/|\.within\.website/)
  not client_ip 203.0.113.0/24 198.51.100.10
}
```

If ONI sits behind another reverse proxy or a CDN, Caddy sees that hop's IP
unless you tell it whom to trust. Configure [`trusted_proxies`][trusted] and
`client_ip_headers` in a global options snippet.

[trusted]: https://caddyserver.com/docs/caddyfile/options#trusted-proxies
