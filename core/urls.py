from django.urls import path
from .views import HomeView
from account.views import UserRegistrationView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
