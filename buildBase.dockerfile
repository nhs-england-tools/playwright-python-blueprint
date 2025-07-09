# This dockerfile allows for the code from the project to be built into a Docker image,
# for use in a CI/CD-style environment such as GitHub Actions or Jenkins.
# Further reading on this: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/

FROM python:3.13-slim

# Create non-root OS user/group and configure environment
RUN addgroup --system nonroot \
  && adduser --system --home /home/nonroot nonroot --ingroup nonroot

WORKDIR /test

ENV HOME=/home/nonroot
ENV PATH="$HOME/.local/bin:$PATH"

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
  playwright install --with-deps && \
  mkdir -p /tests/ && \
  mkdir -p /utils/ && \
  mkdir -p /pages/

# Copy project files
COPY ./tests/ ./tests/
COPY ./utils/ ./utils/
COPY ./pages/ ./pages/
COPY ./conftest.py ./conftest.py
COPY ./pytest.ini ./pytest.ini
COPY ./run_tests.sh ./run_tests.sh
COPY ./users.json ./users.json

# Set permissions, make the script executable and switch OS user
RUN chmod +x ./run_tests.sh \
  && chown -R nonroot:nonroot /test

USER nonroot
