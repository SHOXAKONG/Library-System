from django.urls import path

from book.views import helloworld, get_all_books

urlpatterns = [
    path('hello-world/', helloworld, name='hello-world'),
    path('get_all_books/', get_all_books, name='get_all_books')
]