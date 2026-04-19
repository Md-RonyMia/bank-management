from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserBankAccount,UserAddress
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django.views.generic import UpdateView


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
        fields=['username','first_name','last_name','email','password1','password2','birth_date','account_type','gender','street_address','city','postal_code','country']       

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

            UserAddress.objects.create(
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
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class':'form-control form-control-sm mb-2',
                    'placeholder':self.fields[field].label,
                    
                }
            )
class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-sm mb-2',
                'placeholder': self.fields[field].label,
            })

        try:
            user_address = self.instance.address
            user_account = self.instance.account
        except:
            user_address = None
            user_account = None

        if user_account:
            self.fields['account_type'].initial = user_account.account_type

        if user_address:
            self.fields['street_address'].initial = user_address.street_address
            self.fields['city'].initial = user_address.city
            self.fields['postal_code'].initial = user_address.postal_code
            self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            user_account, _ = UserBankAccount.objects.get_or_create(user=user)
            user_address, _ = UserAddress.objects.get_or_create(user=user)

            user_account.account_type = self.cleaned_data['account_type']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user