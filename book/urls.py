
from django.urls import path

from book.views import get_all_books, get_all_author, home, update_book

urlpatterns = [
    path('', home, name='home'),
    path('books/', get_all_books, name='books_list'),
    path('authors/', get_all_author, name='authors_list'),
    path('update/', update_book, name='update-book'),
]