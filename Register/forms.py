from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.urls import reverse
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator

from .models import User

class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','alias') #Mandatory fields

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        #user.is_active = False #send confirmation email
        if commit:
            user.save()
            self.send_account_activation_email(user)
        return user

    def send_account_activation_email(self,user):
        text_content = 'Account Activation Email'
        subject = 'PIA Toolkit Account Activation'
        template_name = "activation.html"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = [user.email]
        kwargs = {
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            "token": default_token_generator.make_token(user)
        }
        activation_url = reverse("activate_user_account", kwargs=kwargs)
        domain="https://pia-manager.safewave.es"
        activate_url = "{0}{1}".format(domain, activation_url)
        context = {
            'user': user,
            'activate_url': activate_url
        }
        html_content = render_to_string(template_name, context)
        email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        email.attach_alternative(html_content, "text/html")
        email.send()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','alias')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'admin','active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]