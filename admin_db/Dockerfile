FROM python:3.6

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY admin_db.py /usr/src/app/

EXPOSE 5002

CMD ["python", "/usr/src/app/admin_db.py"]
