FROM python:3.13-slim

WORKDIR /test

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps
RUN playwright install chrome

RUN mkdir -p /tests/
COPY ./tests/ ./tests/
RUN mkdir -p /utils/
COPY ./utils/ ./utils/
COPY ./pytest.ini ./pytest.ini
COPY ./run_tests.sh ./run_tests.sh

RUN chmod +x ./run_tests.sh
