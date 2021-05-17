FROM python:3 as development_image

ENV SERVER_IP="0.0.0.0"
ENV SERVER_PORT="8080"
ENV OUTPUT_DIR="/usr/src/app-receiver/output"
ENV DECRYPTION_KEY="/run/secrets/decryption_key"

EXPOSE 8080

WORKDIR /app-receiver
RUN mkdir -p receiver/service
RUN mkdir tests
COPY receiver/service/* receiver/service/
COPY tests/* tests/
COPY receiver/* receiver/

COPY Pipfile ./
COPY Pipfile.lock ./

RUN mkdir -p /usr/src/app-receiver/output
RUN pip install --no-cache-dir pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN pip install pytest

RUN ["pytest", "tests"]


####################################################
FROM python:3 as production_image

ENV SERVER_IP="0.0.0.0"
ENV SERVER_PORT="8080"
ENV OUTPUT_DIR="/usr/src/app-receiver/output"
ENV DECRYPTION_KEY="/run/secrets/decryption_key"

EXPOSE 8080
WORKDIR /receiver
RUN mkdir -p service
COPY --from=development_image /app-receiver/receiver/service/* service/
COPY --from=development_image /app-receiver/receiver/* ./

COPY Pipfile ./
COPY Pipfile.lock ./

RUN mkdir -p /usr/src/app-receiver/output
RUN pip install --no-cache-dir pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["gunicorn", "server:app"]


