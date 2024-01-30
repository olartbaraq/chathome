from django.contrib import admin
from django.urls import path
from user_control.views import login, register_user
from chat_control.views import get_user_lists, get_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_user, name="register"),
    path("login/", login, name="login"),
    path("chat/users/", get_user_lists, name="all_users"),
    path("chat/users/<email>", get_user, name="get_user_by_email"),
]
