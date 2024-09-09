from rest_framework import serializers
from .models import CapitalCall
from bill.serializers import BillSerializer
from investor.serializers import InvestorSerializer
class CapitalCallSerializer(serializers.ModelSerializer):
    bills = BillSerializer(many=True)
    investor = InvestorSerializer()
    class Meta:
        model = CapitalCall
        fields = ['id', 'investor', 'total_amount', 'bills', 'created_date', 'status']
