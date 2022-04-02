1. Run django server

1.1> cmd prompt
set DATABASE_URL=postgres://postgres:root@localhost:5432/gotolong
set DATABASE_URL=mysql://root:root@localhost:3306/gotolong
cd c:/GoogleDrive/my_github/GitHub/gotolong
python manage.py runserver

1.2> bash prompt
export DATABASE_URL=mysql://root:root@localhost:3306/gotolong
export DATABASE_URL=postgres://postgres:root@localhost:5432/gotolong
cd /c/GoogleDrive/my_github/GitHub/gotolong
python manage.py runserver

2. gunicorn
d:
cd c:/GoogleDrive/my_github/GitHub/gotolong-webapp
gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application
# check value of WSGI_APPLICATION in mysite/settings.py

3. collect static files : Heroku : collect static files in /static
python manage.py collectstatic
put something in /static/ (admin files)