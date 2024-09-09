from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CapitalCall
from bill.models import Bill
from investor.models import Investor
from django.db.models import Sum
from .serializers import CapitalCallSerializer
class GenerateCapitalCallView(APIView):
    def post(self, request, investor_id):
        try:
            # Fetch the investor
            investor = Investor.objects.get(id=investor_id)

            # Get the list of bill IDs from the request
            bill_ids = request.data.get('bill_ids', [])
            if not bill_ids:
                return Response({"detail": "No bills selected for generating capital call."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Fetch validated bills that match the provided bill IDs
            validated_bills = Bill.objects.filter(id__in=bill_ids, investor=investor, bill_status='validated')

            if not validated_bills.exists():
                return Response({"detail": "No validated bills found for the given IDs."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if any of the selected bills are already in a capital call
            already_in_capital_call = validated_bills.filter(capitalcall__isnull=False).exists()
            if already_in_capital_call:
                return Response({"detail": "One or more selected bills are already included in a capital call."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Calculate the total amount of the selected validated bills
            total_amount = validated_bills.aggregate(Sum('amount'))['amount__sum']

            # Create the capital call
            capital_call = CapitalCall.objects.create(
                investor=investor,
                status='pending',
                total_amount=total_amount
            )

            # Add selected validated bills to the capital call
            capital_call.bills.set(validated_bills)
            capital_call.save()

            # Return a successful response with the capital call details
            return Response({
                "investor_id": investor.id,
                "investor_name": investor.name,
                "investor_email": investor.email,
                "investor_iban": investor.iban,
                "total_amount": capital_call.total_amount,
                "Date": capital_call.created_date,
                "status": capital_call.status,
                "detail": "Capital call generated successfully."
            }, status=status.HTTP_201_CREATED)

        except Investor.DoesNotExist:
            return Response({"detail": "Investor not found."},
                            status=status.HTTP_404_NOT_FOUND)
    def get(self, request, investor_id):
        try:
            # Fetch the investor
            investor = Investor.objects.get(id=investor_id)

            # Get all capital calls for this investor
            capital_calls = CapitalCall.objects.filter(investor=investor)

            if not capital_calls.exists():
                return Response({"detail": "No capital calls found for this investor."},
                                status=status.HTTP_404_NOT_FOUND)

            # Serialize the capital calls
            serializer = CapitalCallSerializer(capital_calls, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Investor.DoesNotExist:
            return Response({"detail": "Investor not found."},
                            status=status.HTTP_404_NOT_FOUND)
class UpdateCapitalCallStatusView(APIView):
    def post(self, request, capital_call_id):
        new_status = request.data.get('status')
        try:
            capital_call = CapitalCall.objects.get(id=capital_call_id)
            if capital_call.update_status(new_status):
                return Response({"detail": "Capital Call status updated successfully."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid status provided."}, status=status.HTTP_400_BAD_REQUEST)
        except CapitalCall.DoesNotExist:
            return Response({"detail": "Capital Call not found."}, status=status.HTTP_404_NOT_FOUND)
        
class CapitalCallDetailView(APIView):
    def get(self, request, pk):
        try:
            capital_call = CapitalCall.objects.get(pk=pk)
        except CapitalCall.DoesNotExist:
            return Response({"error": "Capital Call not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapitalCallSerializer(capital_call)
        return Response(serializer.data, status=status.HTTP_200_OK)