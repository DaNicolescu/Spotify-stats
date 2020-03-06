FROM python:3

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY client.py /usr/src/app/

EXPOSE 5000

CMD ["python", "/usr/src/app/client.py"]
