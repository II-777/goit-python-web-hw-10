### goit-python-web-hw-10

### Notes:
### 1. Initial Setup
```bash
# To create and start python3 virtual environment
py -m venv .venv
source .venv/bin/activate
# To install required python3 modules
pip install django
# To create a new django project
django-admin startproject base
rsync -a base/* . && rm -rf base/{manage.py,base}
py manage.py startapp quotes
py manage.py startapp users
py manage.py migrate
```

### 2. Setup urls, views, templates and static files
```bash
mkdir quotes/templates
mkdir quotes/templates/quotes
touch quotes/templates/quotes/base.html
touch quotes/templates/quotes/index.html
touch quotes/urls.py

mkdir users/templates
mkdir users/templates/users
touch users/urls.py
```

### add new views in qutes/views.py
```python
# quotes/views.py
...
from django.shortcuts import render

def main(request):
    return render(request, 'quotes/index.html', context={})
```

### add new routes in base/urls.py
```python
### base/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("quotes.urls")),
]
```
### add new routes in quotes/urls.py
```python
### quotes/urls.py
from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name='root'),
]
```

### retister new apps in base/settings.py
```python
# base/settings.py
...
INSTALLED_APPS = [
    ...
    'quotes',
    'users'
]
...
```

### add static files:
```bash
mkdir quotes/static
mkdir quotes/static/quotes
touch quotes/static/quotes/bootstrasp.css
touch quotes/static/quotes/main.css
```

### add links to the static files in the templates:
```html
<!-- # qutes/templates/base.html  -->
...
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    {% load static %}
    <link rel="stylesheet" type="text/css" href="{% static 'quotes/bootstrap.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'quotes/main.css' %}">
...
```

### extend index html using the following syntax 
```html
<!-- # qutes/templates/index.html  -->
{% extends 'quotes/base.html' %}
{% block content %}
...
{% endblock %}
```

### 3.1 Add database data 
```bash
mkdir utils
touch utils/authors.json
touch utils/quotes.json
touch utils/add_quotes_to_mongo.py
touch quotes/utils.py
```

```python
# quotes/utils.py
from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")
    db = client.hw
    return db
```

```python
# quotes/views.py
...
from .utils import get_mongodb


def main(request):
    db = get_mongodb()
    quotes = db.quotes.find()
    return render(request, 'quotes/index.html', context={'quotes': quotes})
```

```python
# utils/add_quotes_to_mongo.py
import json
from bson.objectid import ObjectId
from pymongo import MongoClient

# Connect to the MongoDB server running on localhost
client = MongoClient("mongodb://localhost")

# Select the "hw" database
db = client.hw

# Open the 'quotes.json' file in read mode with UTF-8 encoding
with open('quotes.json', 'r', encoding='utf-8') as file:
    # Load the JSON data from the file into the 'quotes' variable
    quotes = json.load(file)

# Iterate through each quote in the loaded JSON data
for quote in quotes:
    # Query the 'authors' collection to find an author with the specified full name
    author = db.authors.find_one({'fullname': quote['author']})

    # Check if an author is found
    if author:
        # Insert a new document into the 'quotes' collection with quote text, tags, and a reference to the author
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            'author': ObjectId(author['_id'])
        })
```

### 3.2 Add database data 
```bash
mkdir quotes/templatetags
touch quotes/templatetags/extract.py
```

### fix author name display 
```python
# quote/templatetags/extract.py
from django import template
from bson.objectid import ObjectId
from ..utils import get_mongodb

register = template.Library()


def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    if author:
        return author.get('fullname', 'Unknown')
    else:
        return 'Unknown'

register.filter('author', get_author)
```

### utilize {% load extract %} and {{quote.author|author}} constructs in the index.html
```html
<!-- # quotes/index.html -->
{% extends 'quotes/base.html' %}
{% load extract %}
...
<span>by <small class="author" itemprop="author">{{quote.author|author}}</small>
...
```

### 4. Pagination
- [link django docs: pagination](https://docs.djangoproject.com/en/5.0/topics/pagination/)

### Add routes for the paginated quotes
```python
# quotes/urls.py
...
urlpatterns = [
    ...
    path("<int:page>", views.main, name="root_paginate"),
]
```

### Add pagination logic in views.py
```python
# quotes/vies.py
from django.shortcuts import render
from django.core.paginator import Paginator
from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    page = int(page)
    page = max(page, 1)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
```

### Add if-statements in the quotes/index.html based on the pagination, e.g:
```html
...
<li class="previous{% if not quotes.has_previous %} visually-hidden{% endif %}">
...
```

### 5. MongoDB to Postgres migration
- [link django docs: querysets](https://docs.djangoproject.com/en/5.0/ref/models/querysets/)


### add quotes/models.py file:
```python
# quotes/models.py
from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=50, null = False, unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    quote =models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### create utils/migration.py 
```python
# utils/migration.py
import os
import django
from pymongo import MongoClient
import sys

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from quotes.models import Author  # noqa

client = MongoClient("mongodb://localhost")
db = client.hw

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )
```

### Execute utils/migration.py as a module
```bash
# utils/migration.py
py -m utils.migration
```
