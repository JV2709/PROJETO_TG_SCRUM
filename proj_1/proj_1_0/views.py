from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
import requests
import json
import time

def home(request):
    return render(request, 'home.html')

def get_stock_data(request):
    cache_key = 'stock_data_cache'
    
    stock_data_cached = cache.get(cache_key)
    if stock_data_cached:
        return JsonResponse(stock_data_cached, safe=False)
    
    api_key ='VUGWG583Z77XYTYU'
    
    symbols = [
         'NFLX', 'NVDA',
        'PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'ABEV3.SA'
    ]
    
    stock_data = []
    
    for symbol in symbols:
        url =f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if "Error Message" in data:
                continue
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                stock_data.append({
                    'symbol': quote['01. symbol'],
                    'price': quote['05. price'],
                    'change_percent': quote['10. change percent']
                })
        except requests.exceptions.RequestException as e:
            continue
            
        time.sleep(1.5)

    cache.set(cache_key, stock_data, 300)
    
    return JsonResponse(stock_data, safe=False)