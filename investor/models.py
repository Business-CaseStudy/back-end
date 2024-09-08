from django.db import models

# Create your models here.

class Investor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34)
    investment_amount= models.DecimalField(max_digits=10, decimal_places=2)
    investment_date = models.DateField()


    def _str_(self):
        return self.name