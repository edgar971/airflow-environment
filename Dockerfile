FROM fedora:28

ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV AIRFLOW_GPL_UNIDECODE yes

USER root
RUN dnf install -y nmap python3-devel python3-pip python3-Cython gcc-c++ \
  && dnf install -y wget p7zip rsync \
  && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

WORKDIR ${AIRFLOW_HOME}

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt


COPY entrypoint.sh entrypoint.sh
COPY airflow.cfg airflow.cfg

RUN chown -R airflow: ${AIRFLOW_HOME} && chmod +x ./entrypoint.sh

EXPOSE 8080 5555 8793

USER airflow

ENTRYPOINT ["./entrypoint.sh"]