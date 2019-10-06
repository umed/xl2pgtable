FROM openjdk:8-jre-slim

ARG VERSION=6.1.5
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
        libswt-gtk-4-jni \
        libswt-gtk-4-java \
        wget \
    && rm -rf /var/lib/apt/lists/*


RUN wget https://github.com/dbeaver/dbeaver/releases/download/${VERSION}/dbeaver-ce_${VERSION}_amd64.deb \
    && dpkg -i dbeaver-ce_${VERSION}_amd64.deb \
    && rm dbeaver-ce_${VERSION}_amd64.deb

ENV DBEAVER_VERSION=${VERSION}

ENTRYPOINT dbeaver & tail -f temp.log
