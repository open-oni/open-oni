FROM docker.io/golang:1-alpine AS build

RUN apk update && apk upgrade
RUN apk add make git

WORKDIR /usr/local/src/turnstile-proxy
RUN git clone https://github.com/uoregon-libraries/turnstile-proxy-server.git -b v1.0.1-rc3 .
RUN make

FROM alpine AS app
WORKDIR /usr/local/tps
COPY --from=build /usr/local/src/turnstile-proxy/bin/tps tps

# Env values we don't need to let the user configure
ENV GIN_MODE=release
ENV BIND_ADDR=:8080
ENV PROXY_TARGET=http://web:8081

ENTRYPOINT ["/usr/local/tps/tps"]
CMD ["serve"]
