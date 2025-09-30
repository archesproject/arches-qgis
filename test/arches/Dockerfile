FROM ubuntu:22.04
USER root

# Install basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    lsb-release \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC    
ENV PYTHONUNBUFFERED=1

# Install python version
ARG PYTHON_VERSION=${PYTHON_VERSION}
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*    

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    gcc \
    build-essential \
    mime-support \
    libgdal-dev \
    dos2unix \
    nano \
    git \
    postgresql-client-14 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create venv
RUN python${PYTHON_VERSION} -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

ARG ARCHES_PROJECT
ARG ARCHES_PATH=./arches
ARG ARCHES_VERSION

RUN pip install arches==${ARCHES_VERSION}

## Setting default environment variables
ENV WEB_ROOT=/web_root
ENV APP_ROOT=${WEB_ROOT}/${ARCHES_PROJECT}
# ENV AHER_ROOT=${WEB_ROOT}/arches_her
# ENV PKG_ROOT=${APP_ROOT}_package
# ENV DATA_ROOT=${APP_ROOT}_data

# Root project folder
# ENV ARCHES_ROOT=${WEB_ROOT}/arches
ENV WHEELS=/wheels
ENV NODE_VERSION 16.20.1

RUN mkdir ${WEB_ROOT}

# Install packages required to run Arches
# Note that the ubuntu/debian package for libgdal1-dev pulls in libgdal1i, which is built
# with everything enabled, and so, it has a huge amount of dependancies (everything that GDAL
# support, directly and indirectly pulling in mysql-common, odbc, jp2, perl! ... )
# a minimised build of GDAL could remove several hundred MB from the container layer.
RUN set -ex \
    && RUN_DEPS=" \
        build-essential \
        libxml2-dev \
        libproj-dev \
        libjson-c-dev \
        xsltproc \
        docbook-xsl \
        docbook-mathml \
        libgdal-dev \
        libpq-dev \
        mime-support \
        python3-dev \
        postgresql-client-14 \
        dos2unix \
        wait-for-it \
        nano \
    " \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && curl -sL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/postgresql.list \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# nvm environment variables
ENV NVM_DIR /usr/local/nvm
RUN mkdir $NVM_DIR

# install nvm
# https://github.com/nvm-sh/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash -

# install node and npm
RUN echo "source $NVM_DIR/nvm.sh \
  && nvm install $NODE_VERSION \
  && nvm alias default $NODE_VERSION \
  && nvm use default" | bash -

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN npm install -g yarn && apt install wait-for-it

RUN rm -rf /root/.cache/pip/*


# create a new Arches project
WORKDIR ${WEB_ROOT}
RUN arches-admin startproject ${ARCHES_PROJECT} 

WORKDIR ${APP_ROOT}
RUN rm -rf node_modules
RUN rm -f package-lock.json
# Now do the NPM install
RUN npm install

COPY ./settings_local.py ${APP_ROOT}/${ARCHES_PROJECT}/settings_local.py

# Make sure the entry point is available and lacks weird characters
# that don't work in a Linux OS
COPY ./entrypoint.sh entrypoint.sh
RUN chmod -R 700 entrypoint.sh && \
  dos2unix ${APP_ROOT}/entrypoint.sh

# WORKDIR ${APP_ROOT}

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
CMD ["run_arches"]

# Expose port 8000 or other django port
ARG DJANGO_PORT
EXPOSE ${DJANGO_PORT}