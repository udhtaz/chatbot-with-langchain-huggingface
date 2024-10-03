FROM python:3.9

WORKDIR /app

ARG SECRET_KEY
ARG HUGGINGFACEHUB_API_TOKEN
ARG ENVIRONMENT

# Set default environment variable if not provided
ENV ENVIRONMENT=${ENVIRONMENT:-development}
ENV SECRET_KEY=$SECRET_KEY
ENV HUGGINGFACEHUB_API_TOKEN=$HUGGINGFACEHUB_API_TOKEN

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./
EXPOSE 80
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]