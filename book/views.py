from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

def helloworld(request):
    html_ = '<h1>Hello World!</h1>'
    return HttpResponse(html_)

def get_all_books(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {"books" : books})

