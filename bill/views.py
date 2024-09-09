
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import  Bill
from investor.models import Investor
from datetime import date
from django.db.models import Q, Count, Sum
from .serializers import BillSerializer
from .serializers import InvestorWithBillsSerializer
from django.utils import timezone
from datetime import datetime

class GenerateBillView(APIView):
    def post(self, request, investor_id):
        bill_type = request.data.get('bill_type')
        fee_percentage = request.data.get('fee_percentage')
        due_date = request.data.get('date')
        investment_amount= request.data.get('investment_amount')
        investment_date = request.data.get('investment_date')

        try:
            investor = Investor.objects.get(id=investor_id)
            amount = 0
            parsed_date = datetime.strptime(investment_date, '%Y-%m-%d').date()

            if bill_type == 'membership':
                amount = Bill.calculate_membership_fee(investment_amount)
            elif bill_type == 'upfront':
                amount = Bill.calculate_upfront_fee(investment_amount, fee_percentage)
            elif bill_type == 'yearly':
                amount = Bill.calculate_yearly_fee(parsed_date,investment_amount, fee_percentage)
            else:
                return Response({"error": "Invalid bill type"}, status=status.HTTP_400_BAD_REQUEST)

            bill = Bill.objects.create(
                investor=investor,
                bill_type=bill_type,
                amount=amount,
                due_date=due_date,
                bill_status='pending',
                investment_amount=investment_amount,
                investment_date=investment_date,

            )

            return Response({
                "id": bill.id,
                "investor": investor.id,
                "bill_type": bill.bill_type,
                "amount": bill.amount,
                "due_date": bill.due_date,
                "bill_status": bill.bill_status,
            }, status=status.HTTP_201_CREATED)

        except Investor.DoesNotExist:
            return Response({"error": "Investor not found"}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):

        bills = Bill.objects.values('investor').annotate(
            total_amount=Sum('amount'),
            bill_count=Count('id'),
            pending_count=Count('id', filter=Q(bill_status='pending')),
            validated_count=Count('id', filter=Q(bill_status='validated')),
            paid_count=Count('id', filter=Q(bill_status='paid'))
        ).order_by('investor')

        # Get investor details
        result = []
        for bill in bills:
            investor = Investor.objects.get(id=bill['investor'])
            result.append({
                'investor_id': investor.id,
                'investor_name': investor.name,
                'investor_iban': investor.iban,
                'total_amount': bill['total_amount'],
                'bill_count': bill['bill_count'],
                'pending_count': bill['pending_count'],
                'validated_count': bill['validated_count'],
                'paid_count': bill['paid_count'],
            })

        return Response(result, status=status.HTTP_200_OK)
  
class GenerateBillView2(APIView):
    def post(self, request):
        bill_ids = request.data.get('bill_ids', [])

        if not bill_ids:
            return Response({"detail": "No bill IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        validated_bills = []
        errors = []

        for bill_id in bill_ids:
            try:
               
                bill = Bill.objects.get(id=bill_id)

                
                if bill.bill_status in ['validated', 'paid']:
                    errors.append(f"Bill with ID {bill_id} is already validated or paid.")
                else:
                   
                    bill.bill_status = 'validated'
                    bill.save()
                    validated_bills.append(bill_id)

            except Bill.DoesNotExist:
                errors.append(f"Bill with ID {bill_id} not found.")

        response_data = {
            "validated_bills": validated_bills,
            "errors": errors
        }

        if errors:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_200_OK)    
    def get(self, request, investor_id):
        try:
           
            investor = Investor.objects.get(id=investor_id)
            bills = Bill.objects.filter(investor=investor)
            serializer = InvestorWithBillsSerializer(investor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Investor.DoesNotExist:
            return Response({"error": "Investor not found"}, status=status.HTTP_404_NOT_FOUND)