from django.urls import path

from payments import views

urlpatterns = [
    path("", views.UserList.as_view(), name="user_list"),
    path(
        "<int:pk>/user_balance_update",
        views.UserBalanceUpdateFormView.as_view(),
        name="user_balance_update",
    ),
]
