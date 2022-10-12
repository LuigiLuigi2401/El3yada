from re import template
from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns=[
    path("",authviews.LoginView.as_view(template_name="login.html"),name="login"),
    path("logout/",authviews.LogoutView.as_view(template_name="logout.html"),name="logout")
]