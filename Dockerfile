FROM python:3.10.9

WORKDIR /handAsMouse

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]
