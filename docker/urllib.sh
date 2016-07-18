# Just a collection of things to parse a URL in bash.  Because I'm just that
# crazy.  Used by dev.sh to ensure APP_URL makes sense.

# Strips the protocol from the beginning of a URL and echoes it
_protocol() {
  local url=${1:-}
  echo ${url%%://*}
}

# Strips the host and port from a URL and echoes them
_hostport() {
  local url=${1:-}
  local noproto=${url##*://}
  echo ${noproto%%/*}
}

# Strips the host from a URL and echoes it
_host() {
  local url=${1:-}
  local hp=$(_hostport $url)
  if [[ $hp =~ ':' ]]; then
    echo ${hp%%:*}
  else
    echo $hp
  fi
}

# Strips the port from a URL and echoes it
_port() {
  local url=${1:-}
  local hp=$(_hostport $url)
  if [[ $hp =~ ':' ]]; then
    echo ${hp##*:}
  else
    echo ""
  fi
}
