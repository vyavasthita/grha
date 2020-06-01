"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path, include
from django.views.generic import TemplateView
from .views import MilkView, SupplyView, SupplyAddView, SupplyUpdateView, BillView, BillUpdateView, PaymentView, PaymentPayView


app_name = 'milk'

supplyurlpatterns = [
    path('view/', SupplyView.as_view(), name='supply_view'),
    path('add/', SupplyAddView.as_view(), name='supply_add'),
    path('update/', SupplyUpdateView.as_view(), name='supply_update'),
    path('update/<str:pk>/', SupplyUpdateView.as_view(), name='supply_update'),
]

billurlpatterns = [
    path('view/', BillView.as_view(), name='bill_view'),
    path('generate/', BillUpdateView.as_view(), name='bill_generate'),
]

paymentpatterns = [
    path('view/', PaymentView.as_view(), name='payment_view'),
    path('pay/', PaymentPayView.as_view(), name='payment_pay'),
]

urlpatterns = [
    path('', MilkView.as_view(), name='home'),
    path('supply/', include(supplyurlpatterns)),
    path('supply/', include(supplyurlpatterns)),
    path('supply/', include(supplyurlpatterns)),
    path('supply/', include(supplyurlpatterns)),
    path('bill/', include(billurlpatterns)),
    path('bill/', include(billurlpatterns)),
    path('payment/', include(paymentpatterns)),
    path('payment/', include(paymentpatterns)),
]
