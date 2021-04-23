FROM python:3.9-alpine
LABEL mainteiner="Drumbot"
WORKDIR /usr/src/app
ENV TZ=America/Mexico_City
RUN apk add --no-cache g++ make
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]