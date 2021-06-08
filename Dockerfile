FROM python:3.6
RUN apt-get update && apt-get install nano -y
COPY requirements.txt .
RUN pip install --upgrade django
RUN pip install -r requirements.txt
COPY . .
WORKDIR .
