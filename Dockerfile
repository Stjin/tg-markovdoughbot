FROM python:3.7-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Env vars
ENV DB_HOST ${DB_HOST}
ENV DB_NAME ${DB_NAME}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_USERNAME ${DB_USERNAME}
ENV PORT ${PORT}
ENV EXT_PORT ${EXT_PORT}
ENV WEBHOOK_URL ${WEBHOOK_URL}
ENV TOKEN ${TOKEN}

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv default-libmysqlclient-dev

RUN mkdir -p /codebase /storage
ADD .. /codebase
WORKDIR /codebase

RUN pip3 install -r requirements.txt
RUN chmod +x /codebase/bot.py

CMD python3 /codebase/bot.py;
