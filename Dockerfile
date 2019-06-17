# https://hub.docker.com/_/python
FROM python:3.7

ARG LOCAL_UID=1000
ARG LOCAL_GID=1000

RUN  apt update \
  && apt install apt-transport-https \
  && apt clean

RUN apt update \
  && apt install zip \
  && apt install sudo \
  && apt clean \

# Create user and group for application
RUN if ! grep -E "^.*:x:${LOCAL_GID}" /etc/group >> /dev/null; then \
      groupadd -g "${LOCAL_GID}" python; \
    fi \
 && if ! grep -E "^.*:x:${LOCAL_UID}:.*$" /etc/passwd >> /dev/null; then \
      useradd -r -m -s /sbin/nologin -c "Docker application user" -u "${LOCAL_UID}" -g "${LOCAL_GID}" -l python; \
    fi

COPY requirements.txt /tmp/requirements.txt
COPY requirements_dev.txt /tmp/requirements_dev.txt

RUN  pip install --upgrade pip setuptools \
  && pip install -r /tmp/requirements.txt  \
  && pip install -r /tmp/requirements_dev.txt
