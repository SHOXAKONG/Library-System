from django import forms
from .models import Author, Book

class UpdateBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
