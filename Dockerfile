FROM python:3.10.8
WORKDIR /
ADD . /
RUN pip install -r requirements.txt
CMD [ "uwsgi", "app.ini"]