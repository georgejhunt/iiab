FROM alpine:latest
LABEL maintainer Jan Szumiec <jan.szumiec@gmail.com>
ARG KIWIX_VERSION=kiwix-tools_linux-armhf-0.5.0
ARG IIAB_DOWNLOAD_URL=http://download.iiab.io/packages
RUN apk add --no-cache wget gzip
WORKDIR /tmp
RUN wget -cq  ${IIAB_DOWNLOAD_URL}/${KIWIX_VERSION}.tar.gz
RUN tar xzf ${KIWIX_VERSION}.tar.gz
WORKDIR /tmp/$KIWIX_VERSION
RUN mkdir -p /kiwix/bin
RUN mv kiwix-serve /kiwix/bin
RUN rm -rf /tmp/*
WORKDIR /library/zims
EXPOSE 3000
ENTRYPOINT ["/kiwix/bin/kiwix-serve", "--port", "3000", "--library", "/library/zims/library.xml"]


