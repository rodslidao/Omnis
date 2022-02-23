ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/elasticsearch/elasticsearch:${ELK_VERSION}

USER root
RUN mkdir /state && chown elasticsearch /state
USER elasticsearch:root

COPY entrypoint.sh /
COPY helpers.sh /
ENTRYPOINT ["/entrypoint.sh"]
