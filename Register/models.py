# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

from django.utils import timezone

# Create your models here.
# Models to redefine the User model
# Will need to add AUTH_USER_MODEL = 'Register.User' to the settings.py
User = settings.AUTH_USER_MODEL     #For changing the User model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
                    email = self.normalize_email(email)
        )
        user_obj.set_password(password) #change user password
        user_obj.active = is_active
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
                    email,
                    password=password,
                    is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
                    email,
                    password=password,
                    is_active=True,
                    is_staff=True,
                    is_admin=True

        )
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email         = models.EmailField(unique=True)
    alias         = models.CharField(max_length=10)
    date_joined   = models.DateTimeField(default=timezone.now)
    last_login    = models.DateTimeField(default=timezone.now)
    active        = models.BooleanField(default=False)
    staff         = models.BooleanField(default=False)
    admin         = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
     return self.staff

    @property
    def is_admin(self):
     return self.admin

    # @property
    # def is_active(self):
    #     return self.active

