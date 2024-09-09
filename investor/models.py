from django.db import models


class Investor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34)
  
    def _str_(self):
        return self.name