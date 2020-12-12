
1. Run django server
d:
cd d:/GoogleDrive/my_github/GitHub/gotolong/django
python manage.py runserver


3. gunicorn

d:
cd d:/GoogleDrive/my_github/GitHub/gotolong/gotolong-django
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application

# check value of WSGI_APPLICATION in mysite/settings.py


3. collect static files
Heroku : collect static files in /static
d:
cd d:/GoogleDrive/my_github/GitHub/gotolong/gotolong-django
python manage.py collectstatic

put something in /static/ (admin files)


