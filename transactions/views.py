from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import Transactions
from .forms import DepositForm,WithdrawForm, LoanrequestForm, TransferMoneyForm
from .constants import DEPOSIT, WITHDRAWAL, LOAN, LOAN_PAID, TRANSFERMONEY, RECEIVE_MONEY
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import UserBankAccount
from core.models import Bank
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user' : user,
        'amount' : amount
    })
    to_email = user.email
    send_email = EmailMultiAlternatives(subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

# Ei ekta view k inherit kore deposit, withdraw, lone request korbo
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transactions
    title = ''
    success_url = reverse_lazy('transaction_report')
    def get_form_kwargs(self): # form e otirikto data patano hoy # Generating default form data (POST/GET).
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account, # Sending additional data to `account`
        })
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title' : self.title
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transactions_type': DEPOSIT} # defoult babe set korteci man ta
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        # print(amount)
        account = self.request.user.account
        account.balance += amount
        # print(account.balance)
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request, f"{amount}$ was deposit to your account successfully")

        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposit_email.html")

        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw'


    def get_initial(self):
        initial = {'transactions_type' : WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        bank = Bank.objects.get(name="Jomuna bank")
        if not bank.is_bankrupt:
            amount = form.cleaned_data.get('amount')
            account = self.request.user.account
            account.balance -= amount
            account.save(
                update_fields = ['balance']
            )
            messages.success(self.request, f"Successfully withdraw {amount}$ form your account successfully")
            send_transaction_email(self.request.user, amount, "Withdrawal Message", "transactions/withdraw_email.html")
            return super().form_valid(form)
            
        else:
            messages.error(self.request, f"Can't withdraw maney couase bank is bankrupt")
            return redirect('home')

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanrequestForm
    title = 'Request For Loan'


    def get_initial(self):
        initial = {'transactions_type' : LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transactions.objects.filter(account = self.request.user.account, transactions_type = 3, loan_approve = True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have crossed your limits")
        messages.success(self.request, f"Loan request for amount {amount} $ has been successfully sent to admin")
        send_transaction_email(self.request.user, amount, "Loan Request Message", "transactions/loanrequest_email.html")
        return super().form_valid(form)

class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transactions
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    context_object_name = 'report_list'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transactions.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account' : self.request.user.account
        })
        return context

class PayloanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transactions, id=loan_id)

        if loan.loan_approve:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transation = user_account.balance
                user_account.save()
                loan.transactions_type = LOAN_PAID
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(self.request, f"Loan amount is not geterthen avilable balance")
                return redirect('loan_list')

class LoanListView(LoginRequiredMixin, ListView):
    model = Transactions
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans'

    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transactions.objects.filter(account = user_account, transactions_type = LOAN)
        return queryset
    
class TransferMoneyviews(TransactionCreateMixin):
    template_name = 'transactions/transfer_money.html'
    form_class = TransferMoneyForm
    title = 'transfer money'

    def get_initial(self):
        initial = {'transactions_type' : TRANSFERMONEY}
        return initial
    
    # def get_form_kwargs(self): # form e otirikto data patano hoy # Generating default form data (POST/GET).
    #     kwargs = super().get_form_kwargs()
    #     print(kwargs)
    #     if hasattr(self.request.user, 'account'): # hasattr(object, 'attribute') True or False.
    #         kwargs.update({
    #             'account' : self.request.user.account, # Sending additional data to `account`
    #         })
    #     else:
    #         messages.error(self.request, 'Your account is not associated. Please contact support.')
    #         raise ValueError('User account is missing')
    #     return kwargs
    
    def form_valid(self, form):
        account_no = form.cleaned_data.get('account_no')   # Target account
        # print(account_no)
        amount = form.cleaned_data.get('amount') # Transfer amount
        # print(amount)

        target_account = UserBankAccount.objects.get(account_no = account_no)
        target_account.balance += amount
        target_account.save(update_fields = ['balance'])

        receiver_transaction = Transactions(
            amount=amount, transactions_type=RECEIVE_MONEY, account=target_account, balance_after_transation=target_account.balance)
        receiver_transaction.save()

        sender_account = self.request.user.account
        sender_account.balance -= amount
        sender_account.save(update_fields = ['balance'])       

        messages.success(self.request, f"""{
                         amount} has been sent to Account:  {account_no}""")
        return super().form_valid(form)