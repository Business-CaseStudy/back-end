from rest_framework import serializers
from .models import Bill
from investor.models import Investor

# class InvestorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Investor
#         fields = ['id', 'name', 'investment_amount', 'investment_date']  # Adjust fields as needed
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'bill_type', 'bill_status', 'amount', 'due_date', 'created_date']

class InvestorWithBillsSerializer(serializers.ModelSerializer):
    bills = BillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Investor
        fields = ['id', 'name', 'iban','bills']  # Adjust fields as needed