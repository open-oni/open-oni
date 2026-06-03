// Command url-split splits a URL into scheme and host for Caddy headers
package main

import (
	"fmt"
	"net/url"
	"os"
)

func exit(msg string) {
		fmt.Fprintln(os.Stderr, "Error:", msg)
		fmt.Fprintln(os.Stderr)
		fmt.Fprintln(os.Stderr, "usage: url-split <url>")
		os.Exit(1)
}

func main() {
	if len(os.Args) != 2 {
		exit("exactly one arg must be present")
	}

	raw := os.Args[1]
	u, err := url.Parse(raw)
	if err != nil {
		exit(fmt.Sprintf("cannot parse %q: %v", raw, err))
	}

	if u.Host == "" || u.Scheme == "" {
		exit(fmt.Sprintf("cannot parse %q: empty host or scheme", raw))
	}

	fmt.Println(u.Scheme+"|"+u.Host)
}
