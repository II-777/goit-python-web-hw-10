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
