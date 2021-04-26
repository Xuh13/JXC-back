"""JXC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user import views as userviews
from stock import views as stockviews
from record import views as recordviews
from bill import views as billviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test', userviews.test, name='test'),
    url(r'^userlist', userviews.userlist, name='userlist'),
    url(r'^addUsers', userviews.add_users, name='addUsers'),
    url(r'^deleteUser', userviews.deleteUser, name='deleteUser'),
    url(r'^login', userviews.get_login, name='login'),
    url(r'^checktoken', userviews.checkToken, name='checktoken'),

    url(r'^stocklist', stockviews.stocklist, name='stocklist'),
    url(r'^getUnit', stockviews.getunit, name='getUnit'),
    url(r'^warehousing', stockviews.warehousing, name='warehousing'),
    url(r'^setWarning', stockviews.setWarning, name='setWarning'),
    url(r'^outOfStock', stockviews.outofstock, name='outOfStock'),

    url(r'^recordlist', recordviews.recordlist, name='recordlist'),
    url(r'^stockHisRecord', recordviews.stockHisRecord, name='stockHisRecord'),
    url(r'^monthRecord', recordviews.monthRecord, name='monthRecord'),
    url(r'^totalRecord', recordviews.totalRecord, name='totalRecord'),

    url(r'^billlist', billviews.billlist, name='billlist'),

]
