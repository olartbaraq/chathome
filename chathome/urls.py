from django.contrib import admin
from django.urls import path
from chat_control import views
from user_control.views import login, register_user
from chat_control.views import (
    get_user_lists,
    get_user,
    store_email,
    list_emails,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_user, name="register"),
    path("login/", login, name="login"),
    path("chat/users/", get_user_lists, name="all_users"),
    path("chat/users/<str:email>", get_user, name="get_user_by_email"),
    path("chat/users/store_email/", store_email, name="store_email"),
    path("chat/users/list_emails/", list_emails, name="list_emails"),
    path(
        "chat/users/<int:partner_id>/messages/",
        views.MessageList.as_view(),
        name="chat-messages",
    ),
]
