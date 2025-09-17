# proj_1_0/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
import requests
import json
import time
from .models import Card2, CARROSSEL
from decimal import Decimal

# A função home deve buscar os cards e renderizar o template
def home(request):
    card1 = Card2.objects.get(pk=1)
    card2 = Card2.objects.get(pk=2)
    card3 = Card2.objects.get(pk=3)
    
    context = {
        'card1': card1,
        'card2': card2,
        'card3': card3,
    }
    return render(request, 'home.html', context)


# A view para o carrossel agora busca dados do seu banco de dados
def get_stock_data(request):
    cache_key = 'stock_data_cache'
    stock_data_cached = cache.get(cache_key)

    if stock_data_cached:
        return JsonResponse(stock_data_cached, safe=False)

    # Busca todos os itens do carrossel do banco de dados
    ticker_items = CARROSSEL.objects.all()

    stock_data = []
    for item in ticker_items:
        stock_data.append({
            'symbol': item.SIMBOLO,
            'price': str(item.PRECO),
            'change_percent': str(item.VARIACAO),
        })

    cache.set(cache_key, stock_data, 300)

    return JsonResponse(stock_data, safe=False)