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


