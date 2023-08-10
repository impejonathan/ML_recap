FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
        curl \   
        gnupg \ 
        && apt-get -y autoremove \
        && apt-get clean

# Add Microsoft repository for msodbcsql18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install msodbcsql18
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:80" ]


# docker run -p 8000:8000 --rm  -v C:\Users\impej\Documents\BRIEF\ML_recap\cine_prediction:/app impejonathan/django-cine-prediction
# docker run -p 80:80 --rm  -v C:\Users\impej\Documents\BRIEF\ML_recap\cine_prediction:/app impejonathan/django-cine-prediction