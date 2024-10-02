FROM python:3.12-slim

WORKDIR /test

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps
RUN playwright install chrome

COPY ./test_main.py ./test_main.py
COPY ./utility_functions.py ./utility_functions.py
COPY ./conftest.py ./conftest.py
COPY ./pytest.ini ./pytest.ini
COPY ./run_tests.sh ./run_tests.sh
