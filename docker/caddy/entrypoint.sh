#!/bin/sh

set -eu

# Convert `ONI_BASE_URL` into host/scheme parts for Caddy. If this fails,
# something is horribly misconfigured, and it's okay to crash out
raw=$(url-split "$ONI_BASE_URL")
export ONI_PUBLIC_SCHEME=${raw%|*}
export ONI_PUBLIC_HOST=${raw#*|}

echo "Caddy-Int: ONI_PUBLIC_SCHEME=$ONI_PUBLIC_SCHEME"
echo "Caddy-Int: ONI_PUBLIC_HOST=$ONI_PUBLIC_HOST"

exec caddy "$@"
