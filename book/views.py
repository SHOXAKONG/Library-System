from urllib.parse import urlencode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import User
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.views.generic import DetailView, UpdateView

from config import settings
from .models import Book, Author
from .forms import UpdateBook, ForgotPassword, RestorePassword, UpdateAuthor, CreateBook, CreateAuthor
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


@login_required
@permission_required('book.can_manage_books', raise_exception=True)
def create_book(request):
    authors = Author.objects.all()
    if request.method == "POST":
        forms = CreateBook(request.POST, request.FILES)
        if forms.is_valid():
            book = forms.save(commit=False)
            author_id = request.POST.get('author')
            author = Author.objects.filter(id=author_id).first()
            book.author = author
            book.save()
            return redirect('books_list')
        return render(request, 'books/create_book.html', {"forms": forms, "authors": authors})
    forms = CreateBook()
    return render(request, 'books/create_book.html', {"forms": forms, "authors": authors})


@login_required
@permission_required('book.can_manage_books', raise_exception=True)
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


@login_required
@permission_required('book.can_manage_books', raise_exception=True)
def delete_view(request, pk):
    Book.objects.filter(pk=pk).delete()
    return redirect('books_list')


@login_required
@permission_required('book.can_manage_author', raise_exception=True)
def update_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        forms = UpdateAuthor(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('authors_list')
        return render(request, 'authors/update_author.html', {
            "forms": forms,
            "author": author
        })
    forms = UpdateAuthor()
    return render(request, 'authors/update_author.html', {
        "forms": forms,
        "author": author
    })


@login_required
@permission_required('book.can_manage_author', raise_exception=True)
def delete_author(request, pk):
    Author.objects.filter(pk=pk).delete()
    return redirect('authors_list')


@login_required
@permission_required('book.can_manage_author', raise_exception=True)
def create_author(request):
    if request.method == "POST":
        forms = CreateAuthor(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('authors_list')
        return render(request, 'authors/create_author.html', {"forms": forms})
    forms = CreateAuthor()
    return render(request, 'authors/create_author.html', {"forms": forms}
                  )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
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


def logout_view(request):
    logout(request)
    return redirect('login_')


def google_login(request):
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    url = settings.GOOGLE_AUTH_URL + "?" + urlencode(params)

    return redirect(url)


def google_callback(request):
    code = request.GET.get("code")
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return render(request, 'error.html', {"message": "Failed to get access token"})
    user_info_response = requests.get(
        settings.GOOGLE_USERINFO_URL,
        params={"alt": "json"},
        headers={"Authorization": f"Bearer {access_token}"})
    userinfo = user_info_response.json()
    email = userinfo.get("email")
    if not email:
        return render(request, 'error.html', {"message": "Failed to get access token"})

    user = User.objects.filter(email=email).first()
    if not user:
        user = User.objects.create(
            email=email,
            first_name=userinfo.get("given_name", ""),
            last_name=userinfo.get("family_name", ""),
        )

    login(request, user)
    return redirect('/')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['image', 'bio', 'phone_number']
    template_name = 'profile/update.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return self.request.user
