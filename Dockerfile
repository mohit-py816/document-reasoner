FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY .env .

COPY ./requirements.txt .

RUN apt-get update && \
	apt-get install python3-tk \
	tk \
	tcl \
	libgl1-mesa-glx \
	libgl1 \
	libgomp1 \
	build-essential \
	x11-apps \
	libx11-6 \
	cmake -y && \
	rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/models

CMD ["python", "-m", "src.main"]
