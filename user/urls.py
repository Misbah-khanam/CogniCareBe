from django.urls import path
from .views import login_user, register_user,logout_view

urlpatterns = [
    path("login/",login_user , name="login"),
    path("signup/",register_user, name="register"),
    path("logout/",logout_view, name="logout")
]