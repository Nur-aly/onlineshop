from django.urls import path
from .views import user_login, register
from django.contrib.auth.views import *

urlpatterns = [
    path('user_login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/<uidb64>/<token>/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

