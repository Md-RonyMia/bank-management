from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import login

# Create your views here.


class UserRegistraionView(FormView):
    template_name='registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('home')
    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)