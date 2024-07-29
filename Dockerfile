FROM python:3.9.5

WORKDIR /srv

COPY ./requirements.txt /srv/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /srv/requirements.txt

COPY ./ /srv/

CMD ["python", "backend/main.py"]
