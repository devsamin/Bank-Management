from django.contrib import admin
from transactions.models import Transactions
from .views import send_transaction_email
# Register your models here.

@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transation', 'transactions_type','loan_approve']
    def save_model(self, request, obj, form, change):
        if obj.loan_approve == True:
            obj.account.balance += obj.amount
            obj.balance_after_transation = obj.account.balance
            obj.account.save()
            send_transaction_email(obj.account.user, obj.amount, "Loan Approval", "transactions/admin_email.html")
        super().save_model(request, obj, form, change)
