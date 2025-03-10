from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author
from .forms import UpdateBook, ForgotPassword, RestorePassword
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm
from .service import send_email_in_threading


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
        "q": q,
        "books": books
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
        "q": q,
        "authors": authors
    }

    return render(request, 'authors/authors_list.html', context=data)


def update_book(request, pk):
    authors = Author.objects.all()
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        forms = UpdateBook(request.POST, instance=book)
        if forms.is_valid():
            forms.save()
            return redirect('books_list')
        return render(request, 'books/update_book.html', {
            "forms": forms
        })
    forms = UpdateBook()
    return render(request, 'books/update_book.html', {
        "forms": forms,
        "authors": authors
    })


def delete_view(request, pk):
    Book.objects.filter(pk=pk).delete()
    return redirect('books_list')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        return render(request, 'login/login.html', {"form": form})
    form = LoginForm()
    return render(request, 'login/login.html', {"form": form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_')
        return render(request, 'login/register.html', {"form": form})
    form = RegisterForm()
    return render(request, 'login/register.html', {"form": form})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                send_email_in_threading(user.email, user)
                return render(request, "login/reset_password_confirm.html")
            form.add_error("email", "User not found")
        return render(request, "login/forgot_password.html", {"form": form})
    form = ForgotPassword()
    return render(request, 'login/forgot_password.html', {"form": form})


def restore_password(request):
    if request.method == "POST":
        forms = RestorePassword(request.POST)
        if forms.is_valid():
            forms.update()
            return render(request, 'login/reset_password_complete.html', {"forms": forms})
        return render(request, 'login/reset_password.html', {"forms": forms})
    forms = RestorePassword()
    return render(request, 'login/reset_password.html', {"forms": forms})
