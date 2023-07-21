FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# application

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

# migrations

RUN alembic revision --autogenerate

RUN alembic upgrade head


# SOIKA

WORKDIR /app/app/services

RUN git clone https://github.com/Text-Analytics/SOIKA.git

RUN  pip install --no-cache-dir --upgrade -r SOIKA/requirements.txt