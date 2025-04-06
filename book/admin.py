from django.contrib import admin
from book.models import Book, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth']
    ordering = ['full_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'author', 'isbn', 'published_date']
    ordering = ['title', 'price', 'author']