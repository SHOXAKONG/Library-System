from django.contrib import admin
from book.models import Book, Author, FileUpload
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth import get_user_model


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_birth']
    ordering = ['full_name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'author', 'isbn', 'published_date']
    ordering = ['title', 'price', 'author']


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser')}
         ),
    )


@admin.register(FileUpload)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'file', 'created_at', 'is_public']
    list_filter = ['user', 'title']

