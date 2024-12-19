from django.urls import path
from accounts.views import UserRegisterViews, UserLoginview,UserLogoutview,BankaccountUpdateView, passwordchangeviews

urlpatterns = [
    path('register/', UserRegisterViews.as_view(), name="register"),
    path('login/', UserLoginview.as_view(), name="login"),
    path('change_password/',passwordchangeviews, name="change_pass"),
    # path('logout/', Userlogoutview.as_view(), name="logout"),
    path('logout/', UserLogoutview, name="logout"),
    path('profile/', BankaccountUpdateView.as_view(), name="profile")
]