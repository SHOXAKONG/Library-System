from django.contrib.admin.templatetags.admin_list import pagination
from django.db.models import Q
from django.shortcuts import render
from .models import Book, Author
from .forms import UpdateBook
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home/home.html')

def get_all_books(request):
    q = request.GET.get('q', '')
    books = Book.objects.all()
    if q and q != "None":
        books = Book.objects.search(q)

    paginator = Paginator(books, 1)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)
    data = {
        "q" : q,
        "books" : books
    }

    return render(request, 'books/book_list.html', context=data)

def get_all_author(request):
    q = request.GET.get('q', '')
    authors = Author.objects.all()
    if q and q != "None":
        authors = Author.objects.search(q)

    paginator = Paginator(authors, 1)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)
    data = {
        "q" : q,
        "authors" : authors
    }

    return render(request, 'authors/authors_list.html', context=data)

def update_book(request):
    forms = UpdateBook()
    return render(request, 'books/update_book.html', {
        "forms" : forms
    })