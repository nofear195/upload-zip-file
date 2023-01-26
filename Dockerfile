FROM python:3-alpine3.17
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt

