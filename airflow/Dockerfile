FROM apache/airflow:latest-python3.11


ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update -qq && apt-get install vim -qqq && apt-get install tree

COPY requirements.txt .
USER airflow
RUN pip install --no-cache-dir -r requirements.txt
USER root
ENV PATH=$PATH:/root/.local/bin

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

ARG CLOUD_SDK_VERSION=410.0.0
ENV GCLOUD_HOME=/opt/google-cloud-sdk

ENV PATH="${GCLOUD_HOME}/bin/:${PATH}"

RUN DOWNLOAD_URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl -fsSL "${DOWNLOAD_URL}" --output "${TMP_DIR}/google-cloud-sdk.tar.gz" \
    && mkdir -p "${GCLOUD_HOME}" \
    && tar xzf "${TMP_DIR}/google-cloud-sdk.tar.gz" -C "${GCLOUD_HOME}" --strip-components=1 \
    && "${GCLOUD_HOME}/install.sh" \
        --bash-completion=false \
        --path-update=false \
        --usage-reporting=false \
        --additional-components alpha beta kubectl \
        --quiet \
    && rm -rf "${TMP_DIR}" \
    && rm -rf "${GCLOUD_HOME}/.install/.backup/" \
    && gcloud --version


ENV NODEJS=/opt/nodejs
ENV PATH="${NODEJS}/:${PATH}"

# Update the package list and install Node.js and npm
RUN mkdir ${NODEJS} \
    && curl -fsSL https://deb.nodesource.com/setup_20.x -o "${NODEJS}/nodesource_setup.sh" \
    && chmod +x /opt/nodejs/nodesource_setup.sh \
    && ${NODEJS}/nodesource_setup.sh \
    && apt-get install nodejs \
    && npm -v

# Install geojson2ndjson globally using npm
RUN npm install -g geojson2ndjson

# ENV DBT_HOME=/opt/dbt-cloud-cli
# ENV PATH="${DBT_HOME}/:${PATH}"

# RUN TMP_DIR="$(mktemp -d)" \
#     && curl -fL "https://github.com/dbt-labs/dbt-cli/releases/download/v0.38.4/dbt_0.38.4_linux_amd64.tar.gz" --output "${TMP_DIR}/dbt_0.38.4_linux_amd64.tar.gz" \
#     && mkdir -p "${DBT_HOME}" \
#     && tar -xvzf "${TMP_DIR}/dbt_0.38.4_linux_amd64.tar.gz" -C "${DBT_HOME}" \
#     && rm -rf "${TMP_DIR}" \
#     && ${DBT_HOME}/dbt --version


WORKDIR ${AIRFLOW_HOME}

COPY scripts /scripts
RUN chmod -R +x /scripts

USER ${AIRFLOW_UID}