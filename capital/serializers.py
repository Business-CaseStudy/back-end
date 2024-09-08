from rest_framework import serializers
from .models import CapitalCall
from bill.serializers import BillSerializer
class CapitalCallSerializer(serializers.ModelSerializer):
    bills = BillSerializer(many=True)
    class Meta:
        model = CapitalCall
        fields = ['id', 'investor', 'total_amount', 'bills', 'created_date', 'status']
        # fields = '__all__'