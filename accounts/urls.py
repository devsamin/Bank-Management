from django.urls import path
from accounts.views import UserRegisterViews, UserLoginview,UserLogoutview,BankaccountUpdateView

urlpatterns = [
    path('register/', UserRegisterViews.as_view(), name="register"),
    path('login/', UserLoginview.as_view(), name="login"),
    # path('logout/', Userlogoutview.as_view(), name="logout"),
    path('logout/', UserLogoutview, name="logout"),
    path('profile/', BankaccountUpdateView.as_view(), name="profile")
]