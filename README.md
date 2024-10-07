# Project Setup

## Pipenv
- **Install pipenv:** `pip install pipenv`
- **Create & activate virtual environment:** `pipenv shell`
- **Install requirements:** `pipenv install`
- **Add new packages:** `pipenv install package_name`
- **Exit virtual environment:** `exit`

# Django Commands
- **Create a project:** `django-admin startproject projectname`
- **Create an app:** `python manage.py startapp appname`
- **Create migrations:** `python manage.py makemigrations`
- **Apply migrations:** `python manage.py migrate`
- **Create superuser:** `python manage.py createsuperuser`
- **Start development server:** `python manage.py runserver`

# API Endpoints

## Authentication
### Delivery Crew & Manager
- **GET** `/api/groups/delivery-crew/users` - Returns all delivery crew (Manager role).
- **POST** `/api/groups/delivery-crew/users` - Assigns user to delivery crew, 201-Created (Manager role).
- **DELETE** `/api/groups/delivery-crew/users/{userId}` - Removes user from delivery crew, 200-Success or 404-Not found (Manager role).
- **GET** `/api/groups/manager/users` - Returns all managers (Manager role).
- **POST** `/api/groups/manager/users` - Assigns user to manager group, 201-Created (Manager role).
- **DELETE** `/api/groups/manager/users/{userId}` - Removes user from manager group, 200-Success or 404-Not found (Manager role).
- **POST** `/token/login/` - Generates access tokens (Anyone with a valid username and password).
- **POST** `/api/users` - Creates a new user (No role required).
- **GET** `/api/users/me/` - Displays current user (Anyone with a valid user token).

## Cart
- **GET** `/api/cart/menu-items` - Returns current cart items for the user (Customer role).
- **POST** `/api/cart/menu-items` - Adds menu item to cart (Customer role).
- **DELETE** `/api/cart/menu-items` - Deletes all cart items (Customer role).

## Orders
### General
- **GET** `/api/orders` - Returns all orders with items:
  - Customer role: Orders created by this user.
  - Delivery crew role: Orders assigned to delivery crew.
  - Manager role: Orders by all users.
- **POST** `/api/orders` - Creates new order from current cart items, then clears cart (Customer role).
- **GET** `/api/orders/{orderId}` - Returns items for this order, error if ID doesn’t belong to the current user (Customer role).
- **PUT, PATCH** `/api/orders/{orderId}` - Updates order, can set delivery crew and status (Customer role; Manager for setting delivery crew and status).
- **PATCH** `/api/orders/{orderId}` - Updates order status only (Delivery crew role).
- **DELETE** `/api/orders/{orderId}` - Deletes order (Manager role).

## Menu
### General
- **GET** `/api/menu-items/{menuItem}` - Lists all menu items, 200-Ok (Customer, Delivery crew).
- **POST, PUT, PATCH, DELETE** `/api/menu-items/{menuItem}` - Returns 403-Unauthorized (Customer, Delivery crew).
- **GET** `/api/menu-items` - Lists all menu items, 200-Ok (Customer, Delivery crew).
- **POST, PUT, PATCH, DELETE** `/api/menu-items` - Returns 403-Unauthorized (Customer, Delivery crew).
- **GET** `/api/menu-items/{menuItem}` - Lists single menu item (Manager role).
- **PUT, PATCH** `/api/menu-items/{menuItem}` - Updates single menu item (Manager role).
- **DELETE** `/api/menu-items/{menuItem}` - Deletes menu item (Manager role).
- **GET** `/api/menu-items` - Lists all menu items (Manager role).
- **POST** `/api/menu-items` - Creates new menu item, 201-Created (Manager role).

# Testing Users
For testing purposes, there’s a list of users and their credentials in the root folder, in a file called `users.json`.