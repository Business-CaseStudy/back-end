# urls.py
from django.urls import path
from .views import GenerateCapitalCallView, SendCapitalCallByMail,UpdateCapitalCallStatusView,CapitalCallDetailView

urlpatterns = [
    path('generate-capital-call/<int:investor_id>/', GenerateCapitalCallView.as_view(), name='generate-capital-call'),
    path('capital-calls/<int:investor_id>/', GenerateCapitalCallView.as_view(), name='capital-calls-by-investor'),
    path('capitalcall/<int:capital_call_id>/update-status/', UpdateCapitalCallStatusView.as_view(), name='update_capital_call_status'),
    path('capital-call-detail/<int:pk>/', CapitalCallDetailView.as_view(), name='capital-call-detail'),
    path('SendCapitalCallByMail/<int:pk>' , SendCapitalCallByMail.as_view(), name="SendCapitalCallByMail")
]
