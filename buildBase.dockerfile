FROM python:3.13-slim

RUN addgroup --system nonroot \
    && adduser --system --home /home/nonroot nonroot --ingroup nonroot

WORKDIR /test

ENV HOME=/home/nonroot
ENV PATH="$HOME/.local/bin:$PATH"

# Try aws, posgres client install
RUN apt-get update && apt-get --no-install-recommends install -y awscli bash libpq-dev && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/nonroot
ENV PATH="$HOME/.local/bin:$PATH"

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
  playwright install --with-deps && \
  playwright install chrome && \
  mkdir -p /tests/ && \
  mkdir -p /utils/ && \
  mkdir -p /pages/

COPY ./tests/ ./tests/
COPY ./utils/ ./utils/
COPY ./pages/ ./pages/
COPY ./conftest.py ./conftest.py
COPY ./pytest.ini ./pytest.ini
COPY ./run_tests.sh ./run_tests.sh
COPY ./users.json ./users.json

RUN chmod +x ./run_tests.sh \
    && chown -R nonroot:nonroot /test

USER nonroot
