from rest_framework import serializers
from .models import Investor
from .validators import validate_iban
class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'

    def validate_iban(self, value):
        validate_iban(value) 
        return value