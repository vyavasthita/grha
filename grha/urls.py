"""grha URL Configuration

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
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include


# Pattern without language like /milk
urlpatterns = [
    path('admin/', admin.site.urls),
    path('milk/', include('milk.milkurls', namespace = 'nsmilk')),
    path('userauthentication/', include('userauthentication.userauthenticationurls', namespace='nsuserauthentication')),
    path('tenancy/', include('tenancy.tenancyurls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('home.homeurls', namespace='nshome'))
]

# Pattern for language like /hi/milk
urlpatterns += i18n_patterns(
)


# https://www.youtube.com/watch?v=YT60BZJjySg