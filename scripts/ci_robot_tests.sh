#!/bin/bash

echo "Running tests"

# luodaan tietokanta
PYTHONPATH=src poetry run python -m tests.db_helper

echo "DB setup done"

# käynnistetään Flask-palvelin taustalle
TEST_ENV=true PYTHONPATH=src poetry run python -m tests.index &

echo "started Flask server"

# odetetaan, että palvelin on valmiina ottamaan vastaan pyyntöjä
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:5000)" != "200" ]];
  do sleep 1;
done

echo "Flask server is ready"

# suoritetaan testit
poetry run robot --variable BROWSER:firefox --variable HEADLESS:true --exclude clipboard src/tests

status=$?

# pysäytetään Flask-palvelin portissa 5000
kill $(lsof -t -i:5000)

exit $status
