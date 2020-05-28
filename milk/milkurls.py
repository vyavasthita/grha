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


from django.urls import path
from django.views.generic import TemplateView
from .views import MilkView, SupplyView, SupplyUpdateView, BillView, BillUpdateView


urlpatterns = [
    #path('', views.milk, name='milk'),
    path('', MilkView.as_view(), name='milk'),
    path('supply/view/', SupplyView.as_view(), name='supply_view'),
    path('supply/update/', SupplyUpdateView.as_view(), name='supply_update'),
    path('bill/view/', BillView.as_view(), name='bill_view'),
    path('bill/generate/', BillUpdateView.as_view(), name='bill_generate'),
    # path('payment/', views.payment, name='payment'),
]
