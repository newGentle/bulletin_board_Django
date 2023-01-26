from django.urls import path
from .views import SignUp

urlpatterns = [
    path('signup', SignUp.as_view(), name='account_signup'),
    path('login', SignUp.as_view(), name='account_login'),
]