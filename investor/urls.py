from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestorViewSet

router = DefaultRouter()
router.register(r'investors', InvestorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
