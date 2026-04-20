from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Transactions
from .constants import TransactionType, DEPOSIT
from django.contrib import messages
from .forms import TransactionForm,DepositForm,WithdrawalForm,LoanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .constants import DEPOSIT, WITHDRAWAL, LOAN
from django.http import HttpResponse


# Create your views here.

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    model=Transactions
    form_class=TransactionForm
    template_name='transactions/transaction_form.html'
    success_url=reverse_lazy('account:account_detail')
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account
        })
        
        return kwargs
    def get_context_data(self, **kwargs):
         context=super().get_context_data(**kwargs)  
         context.update({
             'title':self.title
             })   

class DepositeMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Deposit'
    def get_initial(self):
        initial={'transaction_type':DEPOSIT}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        account=self.request.user.account
        account.balance+=amount
        account.save({
            update_fields=['balance']
        })

        message.success(self.request,'Money Deposited Successfully')
        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMixin):
    form_class=WithdrawalForm
    title="Withdrawal"
    def get_initial(self):
        initial={'transaction_type':WITHDRAWAL}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        account=self.request.user.account
        account.balance-=amount
        account.save({
            update_fields=['balance']
        })

        messages.success(self.request,'Money Withdrawn Successfully')
        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class=LoanForm
    title="Loan Request"
    def get_initial(self):
        initial={'transaction_type':LOAN}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data['amount']
        current_loan_count=Transactions.objects.filter(account=self.request.user.account, transaction_type=LOAN, loan_approved =True).count()
        if current_loan_count >= 3:
            return httpResponse('Loan limit reached. You cannot request more than 3 loans.')
        account=self.request.user.account
        account.balance+=amount
        account.save({
            update_fields=['balance']
        })

        messages.success(self.request,'Loan Granted Successfully')
        return super().form_valid(form)