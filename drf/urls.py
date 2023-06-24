"""
URL configuration for drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import ForgotPasswordView
from home.views import UserRegistrationView, UserLoginView,PasswordChangeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegistrationView.as_view()),
    path('api/login/', UserLoginView.as_view()),


    path('password/change/', PasswordChangeView.as_view(), name='password_change'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
  #  path('reset-password/<int:user_id>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
]

