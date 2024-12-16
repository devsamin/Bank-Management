from django.db import models
from accounts.models import UserBankAccount
from transactions.constants import TRANSACTION_TYPE
class Transactions(models.Model):
    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='transactons') # Ekjon user multiple transaction korte parbe

    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transation = models.DecimalField(decimal_places=2, max_digits=12)
    transactions_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return str(self.account.account_no)
