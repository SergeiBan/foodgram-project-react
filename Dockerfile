FROM python:3.9-buster
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./backend/ .
COPY ./data data/
RUN python3 manage.py migrate
RUN python3 manage.py add_ingredients
RUN python3 manage.py add_admin_group
RUN python3 manage.py collectstatic --noinput
CMD ["gunicorn", "project.wsgi:application", "--bind", "0:8000"]