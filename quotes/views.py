from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from quotes.models import Author, Quote


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def author_about(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {
        "fullname": author.fullname,
        "born_date": author.born_date,
        "born_location": author.born_location,
        "description": author.description,
    }
    return render(request, "quotes/author_about.html", context)
