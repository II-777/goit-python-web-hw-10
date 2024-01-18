from django.shortcuts import render
from django.core.paginator import Paginator
from .utils import get_mongodb


# Create your views here.
def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    page = int(page)
    page = max(page, 1)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})
