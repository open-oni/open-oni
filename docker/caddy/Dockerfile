# Build our URL parser so Caddy can pass the correct host / scheme to Django if
# a bot protection proxy gets used
FROM docker.io/golang:1-alpine AS build
COPY url-split.go .
RUN CGO_ENABLED=0 go build -o /url-split ./url-split.go

# Now the actual Caddy image
FROM docker.io/caddy:2-alpine
COPY --from=build /url-split /usr/local/bin/url-split
COPY Caddyfile /etc/caddy/Caddyfile
COPY oni-routing.caddyfile /etc/caddy/oni-routing.caddyfile

VOLUME /etc/caddy/conf.d

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]
