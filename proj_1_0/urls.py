from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                                
    path('api/stocks/', views.get_stock_data, name='stock_api'),       
    path('dicionario-do-investidor/', views.DICIONARIO_view, name='dicionario'), 
    path('investimentos/', views.investimentos_view, name='investimentos'),
    path('PERFIL_INVESTIDOR/', views.perfil_investidor_view, name='PERFIL_INVESTIDOR') 
]
