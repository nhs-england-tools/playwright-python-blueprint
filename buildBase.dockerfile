FROM python:3.13-slim

WORKDIR /test

# Install dependencies
# Try posgres client install
RUN apt-get update && apt-get --no-install-recommends install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
  playwright install --with-deps && \
  playwright install chrome && \
  mkdir -p /tests/ && \
  mkdir -p /utils/

COPY ./tests/ ./tests/
COPY ./utils/ ./utils/
COPY ./pytest.ini ./pytest.ini
COPY ./run_tests.sh ./run_tests.sh

RUN chmod +x ./run_tests.sh
