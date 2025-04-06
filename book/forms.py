from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Author, Book, Code
from django.contrib.auth.models import User


class UpdateBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError("Title len should be more than 3")
        return title

class UpdateAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 3:
            raise ValidationError("Full Name Should be more than 3")
        return full_name

class CreateBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class CreateAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=200, widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(max_length=200, widget=forms.PasswordInput, label="Password Confirm")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Password do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class RestorePassword(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(max_length=6)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        code = cleaned_data.get('code')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError("User not found")

        if not Code.objects.filter(user=user, code_number=code, expired_date__gt=timezone.now()):
            raise forms.ValidationError(f"Code is incorrect {timezone.now()}")

        if password != re_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

    def update(self):
        user = User.objects.filter(email=self.cleaned_data.get('email')).first()
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        user.save()

class ForgotPassword(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "form-control"}))

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Email Does Not Exist")
        return email