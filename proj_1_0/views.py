
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
import requests
import json
import time
from .models import Card2, CARROSSEL, DICIONARIO,Investimento
from decimal import Decimal
from itertools import groupby
from .models import PerguntaPerfil

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


def get_stock_data(request):
    cache_key = 'stock_data_cache'
    stock_data_cached = cache.get(cache_key)

    if stock_data_cached:
        return JsonResponse(stock_data_cached, safe=False)

   
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


def DICIONARIO_view(request):
    # Pega todos os termos do banco de dados e os ordena por Categoria e Título.
    terms = DICIONARIO.objects.all().order_by('CATEGORIA', 'TITULO')

    # Agrupa os termos usando a CATEGORIA como critério.
    grouped_terms = {}
    for CATEGORIA, group in groupby(terms, key=lambda x: x.CATEGORIA):
        grouped_terms[CATEGORIA] = list(group)

    context = {
        'grouped_terms': grouped_terms,
    }
    
    return render(request, 'DICIONARIO.html', context)


def investimentos_view(request):
    todos_investimentos = Investimento.objects.all()
    
    context = {
        'investments': todos_investimentos,
    }
    
    return render(request, 'INVESTIMENTOS.html', context)

def perfil_investidor_view(request):
    perguntas = PerguntaPerfil.objects.all()
    context = {'perguntas': perguntas}
    return render(request, 'PERFIL_INVESTIDOR.html', context)
    