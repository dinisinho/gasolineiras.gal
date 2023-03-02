FROM python:3

ENV TZ="Europe/Madrid"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "gasolineiras/gasolineiras.py" ]