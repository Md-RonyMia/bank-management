from django.shortcuts import render
from django.views.generic import FormView,UpdateView
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView,LoginView
from .forms import UserUpdateForm




# Create your views here.


class UserRegistrationView(FormView):
    template_name='userregistration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('home')
    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
class UserUpdateView(UpdateView):
    template_name = 'userprofile.html'
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('userprofile')