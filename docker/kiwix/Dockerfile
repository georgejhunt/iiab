FROM alpine:latest
LABEL maintainer Jan Szumiec <jan.szumiec@gmail.com>
ARG KIWIX_VERSION=kiwix-tools_linux-armhf-0.5.0
RUN apk add --no-cache wget gzip
WORKDIR /
RUN wget -c  http://download.kiwix.org/release/kiwix-tools/${KIWIX_VERSION}.tar.gz
RUN tar xzf ${KIWIX_VERSION}.tar.gz
WORKDIR $KIWIX_VERSION
RUN mkdir -p /kiwix/bin
RUN mv kiwix-* /kiwix/bin
WORKDIR /kiwix-data
VOLUME /kiwix-data
EXPOSE 3000
ENTRYPOINT ["/kiwix/bin/kiwix-serve", "--port", "3000"]


