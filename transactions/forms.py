from django import forms
from .models import Transactions
from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount', 'transactions_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # Accepting `account` sent from view
        super().__init__(*args, **kwargs)
        self.fields['transactions_type'].disabled = True  # Ai fields disabled kora takbe
        self.fields['transactions_type'].widget = forms.HiddenInput() # fields ta user teke hide kora takbe
    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transation = self.account.balance
        return super().save()

class DepositForm(TransactionForm):
    def clean_amount(self): # amount field k filter korbo
        min_deposit_amount = 500
        amount = self.cleaned_data.get('amount') # user fill up kora form teke amount tar value ta nea aslam
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'For you need deposit at least {min_deposit_amount} $'
            )
        return amount
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 15000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at least {min_withdraw_amount} $"
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f"You can withdraw at most {max_withdraw_amount} $"
            )
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} in your account. '
                'you can not more then your account balance'
            )
        return amount

class LoanrequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount

class TransferMoneyForm(TransactionForm):
    account_no = forms.IntegerField()
    class Meta:
        model = Transactions
        fields = ['amount', 'transactions_type']

    def clean_account_no(self):
        account_no = self.cleaned_data.get('account_no')
        if not UserBankAccount.objects.filter(account_no = account_no).exists():
            raise forms.ValidationError('Invalid account no')
        return account_no
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount > self.account.balance:
            raise forms.ValidationError('You dont have enough money') # Amr kase jotesto balance nai
        return amount