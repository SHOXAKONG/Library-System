from django.urls import path

from book.views import get_all_books, get_all_author, home, update_book, login_view, register_view, delete_view, \
    restore_password, forgot_password, create_book, update_author, delete_author, create_author, google_login, \
    google_callback, ProfileView, ProfileUpdateView, FileUploadListView, FileUploadCreate, FileDeleteView, \
    UpdateFileView

urlpatterns = [
    path('', home, name='home'),
    path('books/', get_all_books, name='books_list'),
    path('authors/', get_all_author, name='authors_list'),
    path('update/<int:pk>', update_book, name='update'),
    path('login/', login_view, name='login_'),
    path('register/', register_view, name='register'),
    path('delete/<int:pk>', delete_view, name='delete'),
    path('restore_password/', restore_password, name='restore_password'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('create_book/', create_book, name='create-book'),
    path('update_author/<int:pk>/', update_author, name='update_author'),
    path('delete_author/<int:pk>/', delete_author, name='delete_author'),
    path('create_author/', create_author, name='create_author'),
    path('logout/', login_view, name='logout'),
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
    path('files/', FileUploadListView.as_view(), name='files_list'),
    path('upload/', FileUploadCreate.as_view(), name='upload'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='delete_file'),
    path('update/<int:pk>/', UpdateFileView.as_view(), name='update_file')
]
