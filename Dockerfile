FROM python:3.9
ENV PYTHONBUFFERED 1
RUN mkdir /project_contributors
WORKDIR /project_contributors
COPY ./project_contributors /project_contributors
RUN pip install -r requirements.txt
