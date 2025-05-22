FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV TZ=UTC

RUN apt-get update
RUN apt-get install -y curl

WORKDIR /almaflow

# installing nsq
RUN curl -o nsq-1.3.0.linux-amd64.go1.21.5.tar.gz https://s3.amazonaws.com/bitly-downloads/nsq/nsq-1.3.0.linux-amd64.go1.21.5.tar.gz
RUN tar -xzvf nsq-1.3.0.linux-amd64.go1.21.5.tar.gz
RUN mv nsq-1.3.0.linux-amd64.go1.21.5/bin/nsqd /bin/nsqd

COPY pyproject.toml uv.lock ./
RUN uv sync --all-extras --no-install-project

COPY . .

RUN nsqd & uv run pytest -x
