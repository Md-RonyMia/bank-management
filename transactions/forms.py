from .models import Transactions
from django import forms

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transactions
        fields=['amount','transactions_type']
        
        def __init__(self,*args,**kwargs):
            self.account=kwargs.pop('account')
            super().__init__(*args,**kwargs)
            self.fields['transactions_type'].disabled=True
            self.fields['transactions_type'].widget=forms.HiddenInput()
            
            
            def save(self,commit=True):
                self.instance.account=self.account
                self.instance.balance_after_transaction=self.account.balance
                return super().save()
            
        
        
class DepositForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data['amount']
        minimum_deposit_amount=500
        if amount<=minimum_deposit_amount:
            raise forms.ValidationError('Deposit amount must be at least $%.2f.' % minimum_deposit_amount)
        return amount
    
class WithdrawalForm(TransactionForm):
    def clean_amount(self):
        account=self.account
        minimum_withdrawal_amount=500
        maximum_withdrawal_amount=account.balance
        amount=self.cleaned_data['amount']
        if amount<minimum_withdrawal_amount:
            raise forms.ValidationError('Withdrawal amount must be at least $%.2f.' % minimum_withdrawal_amount)
        if amount>maximum_withdrawal_amount:
            raise forms.ValidationError('Withdrawal amount exceeds available balance.')
        return amount
    
class LoanForm(TransactionForm):
    def clean_amount(self):
        amount=self.cleaned_data['amount']
        return amount