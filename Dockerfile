# Dockerfile for Cyclos project (http://www.cyclos.org)
FROM python:2.7

ENV VDMASK_HOME /root/vdatamask
ADD . ${VDMASK_HOME}
WORKDIR ${VDMASK_HOME}

RUN pip install fake-factory psycopg2 flask && \
    chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
