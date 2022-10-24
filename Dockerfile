FROM python:3.9-buster
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./backend/ .
COPY ./data data/
COPY ./docker-entrypoint.sh .
RUN python3 manage.py collectstatic --noinput
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh"]
CMD ["gunicorn", "project.wsgi:application", "--bind", "0:8000"]