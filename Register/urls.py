from django.urls import reverse_lazy, path, include
from django.contrib.auth import views as auth_views

from Register.views import UserCreateView,activate_user_account

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('new_user/', UserCreateView.as_view(),name='new_user'),
    path('activate/<uidb64>/<token>/',
        activate_user_account, name='activate_user_account'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(),  name='password_reset_complete'),
]