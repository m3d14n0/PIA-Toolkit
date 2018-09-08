# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView

from shared.decorators import staff_only
from .forms import RegisterForm

User = get_user_model()

# Create your views here.
@method_decorator(staff_only, name='dispatch')
class UserCreateView(CreateView):
    template_name = 'create_user.html'
    form_class = RegisterForm
    success_url = reverse_lazy('new_user')
    def form_valid(self,form):
        return super(UserCreateView,self).form_valid(form)

def activate_user_account(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse("Activation link has expired")