## Build & serve mkdocs
FROM python:3.11-slim AS base

## Set ENV variables to control Python/pip behavior inside container
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    ## Pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base AS build

WORKDIR /app

COPY docs/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY mkdocs.yml /app/mkdocs.yml
COPY ./src /app/src
COPY ./docs /app/docs

FROM build AS docs-build

WORKDIR /app

COPY --from=build /app /app

RUN python -m mkdocs build

FROM nginx:alpine AS docs-serve

COPY --from=docs-build /app/site /use/share/nginx/html

RUN cat <<EOF > /etc/nginx/nginx.conf
events {
    worker_connections 1024;
    }

    http {
    include mime.types;
    sendfile on;

    server {
        listen 8000;
        listen [::]:8000;

        resolver 127.0.0.11;
        autoindex off;

        server_name _;
        server_tokens off;

        root /use/share/nginx/html;
        gzip_static on;
    }
}
EOF
