from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserBankAccount,UserAddress
from .constants import ACCOUNT_TYPE,GENDER_TYPE


class UserRegistrationForm(UserCreationForm):
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    account_type=forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=50)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['username','email','password1','password2','birth_date','gender','street_address','city','postal_code','country']       

    def save(self,commit=True):
        user=super().save(commit=False)
        if commit:
            user.save()
            account_type=self.cleaned_data['account_type']
            gender=self.cleaned_data['gender']
            postal_code=self.cleaned_data['postal_code']
            country=self.cleaned_data['country']
            city=self.cleaned_data['city']
            street_address=self.cleaned_data['street_address']
            birth_date=self.cleaned_data['birth_date']

            UserAddess.objects.create(
                user=user,
                postal_code=postal_code,
                country=country,
                city=city,
                street_address=street_address

            )
           UserBankAccount.objects.create(
                user=user,
                account_type=account_type,
                gender=gender,
                birth_date=birth_date,
                account_no=10000+user.id
            )
        return user

     