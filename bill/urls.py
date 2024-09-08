# urls.py
from django.urls import path
from .views import GenerateBillView,GenerateBillView2

urlpatterns = [
    path('generate-bill/<int:investor_id>/', GenerateBillView.as_view(), name='generate-bill'),
    path('group-bills/', GenerateBillView.as_view(), name='group-bills'),
    path('investor/<int:investor_id>/bills/', GenerateBillView2.as_view(), name='investor-bills'),
    path('validate-bill/', GenerateBillView2.as_view(), name='validate-bill'),
]
