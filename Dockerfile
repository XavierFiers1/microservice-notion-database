FROM python:3.11-alpine

ENV PORT=8000
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:app"

RUN apk add build-base

RUN pip install -r requirements.txt

COPY . /app

EXPOSE ${PORT}/tcp

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]