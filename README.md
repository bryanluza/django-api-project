# Project Setup

## Install pipenv
If you haven't installed pipenv yet, you can do so using pip:
`pip install pipenv`

## Create and activate virtual environment
This command creates a new virtual environment (if it doesn't exist) and activates it.
`pipenv shell`

## Install requirements (libraries)
`pipenv install`

## Add new packages
`pipenv install package_name`

## Exit the virtual environment
`exit`

# Django commands
## Create a project
`django-admin startproject projectname`

## Create an app
`python manage.py startapp appname`

## Create migrations
`python manage.py makemigrations`

## Make migrations
`python manage.py migrate`

## Create superuser
`python manage.py createsuperuser`

## Start the development server
`python manage.py runserver`