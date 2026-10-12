from django.db import models

class Account(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    account_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=10)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.account_number
    
    
    
    
    
class TransferTransaction(models.Model):
    sender = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='sent_transfers'
    )
    recipient = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='received_transfers'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.account_number} -> {self.recipient.account_number} : {self.amount}"

