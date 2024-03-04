                                                   
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /steppe
COPY requirements.txt /steppe/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", " 0.0.0.0:8000"]
