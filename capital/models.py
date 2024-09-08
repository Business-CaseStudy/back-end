from django.db import models
from investor.models import Investor
from bill.models import Bill
# Create your models here.

class CapitalCall(models.Model):
    CAPITALCALL_STATUS =[
        ('pending', 'Pending'),
        ('validated', 'validated'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    bills = models.ManyToManyField(Bill)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CAPITALCALL_STATUS)

    def __str__(self):
        return f"Capital Call for {self.investor.name} - Total: {self.total_amount}"
    
    def update_status(self, new_status):
        if new_status in dict(self.CAPITALCALL_STATUS).keys():
            self.status = new_status
            self.save()
            return True
        return False