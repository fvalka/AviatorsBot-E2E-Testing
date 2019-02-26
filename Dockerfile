FROM python:3
LABEL maintainer="aviatorsbot.com"
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY aviatorsbot_e2e ./aviatorsbot_e2e
COPY config ./config
COPY secrets/telegram.session.gpg ./secrets/telegram.session.gpg
COPY tests ./tests
COPY run.sh ./

CMD [ "./run.sh" ]