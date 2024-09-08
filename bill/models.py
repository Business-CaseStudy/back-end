from django.db import models
from investor.models import Investor
from datetime import date
from decimal import Decimal
from django.utils import timezone
# Create your models here.
class Bill(models.Model):
    BILL_TYPE_CHOICES = [
        ('membership', 'Membership'),
        ('upfront', 'Upfront Fees'),
        ('yearly', 'Yearly Fees'),
    ]
    BILL_STATUS =[
        ('pending', 'Pending'),
        ('validated', 'validated'),
        ('paid', 'Paid'),
    ]
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE,related_name='bills')
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES)
    bill_status = models.CharField(max_length=20, choices=BILL_STATUS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    investment_amount= models.DecimalField(max_digits=10, decimal_places=2,default=0)
    investment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.bill_type} - {self.amount} EUR - Due: {self.due_date}"

    @staticmethod
    def calculate_membership_fee(investment_amount):
        if Decimal(investment_amount) > 50000:
            return 0
        return 3000

    @staticmethod
    def calculate_upfront_fee(investment_amount, fee_percentage):
        fee_percentage = Decimal(fee_percentage)

        return fee_percentage * Decimal(investment_amount) * 5

    @staticmethod
    # def calculate_yearly_fee(investor, fee_percentage):
    #     current_year = date.today().year
    #     investment_year = investor.investment_date.year
    #     fee_percentage = Decimal(fee_percentage)

    #     # Yearly fees calculation depending on the investment date and year
    #     if current_year == investment_year:
    #         days_invested = (date.today() - investor.investment_date).days
    #         days_in_year = 365 if (investment_year % 4 == 0 and investment_year % 100 != 0) or (investment_year % 400 == 0) else 365
    #         return (days_invested / days_in_year) * fee_percentage * investor.investment_amount
    #     elif current_year == investment_year + 1:
    #         return fee_percentage * investor.investment_amount
    #     elif current_year == investment_year + 2:
    #         return (fee_percentage - 0.002) * investor.investment_amount
    #     elif current_year == investment_year + 3:
    #         return (fee_percentage - 0.005) * investor.investment_amount
    #     else:
    #         return (fee_percentage - 0.01) * investor.investment_amount
    def calculate_yearly_fee(investment_date,investment_amount, fee_percentage):
        current_year = date.today().year
        investment_year = investment_date.year
        fee_percentage = Decimal(fee_percentage)

        if current_year == investment_year:
            days_invested = (date.today() - investment_date).days
            days_in_year = Decimal(365)  # Convert to Decimal

            # Adjust for leap years
            if (investment_year % 4 == 0 and investment_year % 100 != 0) or (investment_year % 400 == 0):
                days_in_year = Decimal(366)

            return (Decimal(days_invested) / days_in_year) * fee_percentage * Decimal(investment_amount)
        elif current_year == investment_year + 1:
            return fee_percentage * Decimal(investment_amount)
        elif current_year == investment_year + 2:
            return (fee_percentage - Decimal(0.002)) * Decimal(investment_amount)
        elif current_year == investment_year + 3:
            return (fee_percentage - Decimal(0.005)) * Decimal(investment_amount)
        else:
            return (fee_percentage - Decimal(0.01)) * Decimal(investment_amount)