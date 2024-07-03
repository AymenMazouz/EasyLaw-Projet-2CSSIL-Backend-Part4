FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
	pip install -r requirements.txt

COPY . .

EXPOSE 5000
ENV ELASTIC_HOST="https://host.docker.internal:9200"

CMD ["flask", "run", "--host=0.0.0.0"]
