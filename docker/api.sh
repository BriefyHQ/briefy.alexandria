#!/bin/sh
# enable gunicorn in development
if [ ${ENV}="development" ]
then
    COMMAND="gunicorn --paste"
else
    COMMAND="pserve"
fi

export NEW_RELIC_CONFIG_FILE=/app/newrelic.ini

/docker_entrypoint.sh && newrelic-admin run-program ${COMMAND} /app/configs/"${ENV}".ini
