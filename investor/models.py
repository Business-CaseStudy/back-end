from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_iban(value):
    value = value.replace(' ', '')

    if len(value) < 15 or len(value) > 34:
        raise ValidationError("IBAN must be between 15 and 34 characters long.")

    iban_regex = re.compile(r'^FR\d{2}\d{5}\d{11}[A-Z0-9]*$')
    if not iban_regex.match(value):
        raise ValidationError("IBAN format is incorrect.")

class Investor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34, validators=[validate_iban])

    def __str__(self):
        return self.name
