The application is a practical project for a Cyber Security course, and its purpose is to demonstrate five security vulnerabilities.


Installation (macOS, Linux):

1.	Clone repository
2.	Create and activate virtual environment:
      python -m venv .venv
      source .venv/bin/activate
3.	Install requirements: 
      pip install -r requirements.txt
4.	Create database
      python manage.py migrate
5.	Create superuser
      python manage.py createsuperuser
6.	Start program
      python manage.py runserver

Log in to admin site: http://localhost:8000/admin/ using superuser account. Create at least two normal users to test all vulnerabilities. The application is available at http://localhost:8000/todo/ .
