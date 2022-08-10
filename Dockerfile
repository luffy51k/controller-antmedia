FROM python:3.7

WORKDIR /app
RUN mkdir logs

# install supervisord
RUN apt-get update && apt-get install -y supervisor tzdata
ENV TZ="Asia/Ho_Chi_Minh"

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#CMD ["python", "run.py"]
# gunicorn
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]

# needs to be set else Celery gives an error (because docker runs commands inside container as root)
ENV C_FORCE_ROOT=1

# run supervisord
CMD ["/usr/bin/supervisord"]