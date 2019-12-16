#FROM is the base image
FROM ubuntu:16.04



RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY app.py /apps/
COPY config.py /apps/
COPY templates/ /apps/templates/
COPY database.db /apps/
COPY spell_check /apps/
COPY requirements.txt /apps/
COPY admin_ph.txt /apps/
COPY admin_pw.txt /apps/
COPY application_key.txt /apps/

WORKDIR /apps

RUN pip install -r requirements.txt


ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
# CMD ["flask", "run"]

EXPOSE 8080