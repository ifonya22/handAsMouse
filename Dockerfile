FROM python:3.10.9

WORKDIR /handAsMouse

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 python3-tk python3-dev -y

COPY ./app ./app

CMD ["python", "./app/main.py"]
