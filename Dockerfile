FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . /app
COPY ./requirements.txt /requirements.txt

# Set work directory
WORKDIR /app
EXPOSE 8000 

# Create new user
# RUN adduser --disabled-password --no-create-home app


#Make virtual, upgrade pip and install requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt 

# Set user
# USER app

#set path
ENV PATH="/py/bin:$PATH"

# Collect static files during build
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sprintsync.wsgi:application"]