FROM ghcr.io/techarohq/anubis:latest

# Env values we don't need to let the user configure
ENV BIND=:8080
ENV TARGET=http://web:8081
ENV POLICY_FNAME=/etc/anubis/botPolicies.yaml

COPY botPolicies.yaml /etc/anubis/botPolicies.yaml
