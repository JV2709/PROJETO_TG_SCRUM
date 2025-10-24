
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
STOCK_SYMBOLS = [
    'PETR4', 'VALE3', 'ITUB4', 'BBDC4',
    'B3SA3', 'ELET3', 'WEGE3', 'RENT3', 
    'ABEV3', 'BPAC11', 'MGLU3', 'LREN3', 
    'ITSA4' 
]
# Exemplo de URL da Brapi para cotações múltiplas
STOCK_SYMBOLS = [
    'PETR4', 'VALE3', 'ITUB4', 'BBDC4',
    'B3SA3', 'ELET3', 'WEGE3', 'RENT3', 
    'ABEV3', 'BPAC11', 'MGLU3', 'LREN3', 
    'ITSA4' 
]
# URL Base da Brapi para cotação de único ativo (o ticker será adicionado no loop)
API_BASE_URL = "https://brapi.dev/api/quote/" 
# SEU TOKEN AQUI! (Você precisa gerar um token na Brapi ou na API que for usar)
API_KEY = "j1yHtxCLQjGLNPDMdTa3HB" 
# Tempo de cache em segundos (5 minutos)
CACHE_DURATION = 300

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
    """
    Busca dados na API (usando loop para single-ticker), salva no DB, e usa o DB como fallback.
    Ajustado para o formato JSON de resposta que retorna 'results'.
    """
    cache_key = 'stock_data_cache'
    
    # 1. Tenta buscar dados do Cache
    stock_data_cached = cache.get(cache_key)
    if stock_data_cached:
        return JsonResponse(stock_data_cached, safe=False)

    
    new_items_to_save = []
    
    # 2. Tenta buscar dados da API externa, em loop
    try:
        
        # A. Busca os dados de CADA ticker individualmente
        for symbol in STOCK_SYMBOLS:
            
            # Monta a URL completa para o ticker atual
            url = f"{API_BASE_URL}{symbol}?token={API_KEY}"
            
            # Aumentando o timeout para 10 segundos por requisição
            response = requests.get(url, timeout=10) 
            response.raise_for_status() 

            api_data = response.json()
            # 💡 AJUSTE CRÍTICO: Buscar o array na chave 'results'
            api_result_list = api_data.get('results', []) 
            
            if api_result_list:
                stock = api_result_list[0] # Pega o primeiro resultado
                
                # Campos da Brapi
                simbolo = stock.get('symbol', 'N/A')[:10]
                try:
                    # É crucial converter para Decimal
                    preco = Decimal(str(stock.get('regularMarketPrice', 0.0)))
                    # A API retorna a variação em porcentagem (ex: 0.356 para 0.356%)
                    variacao = Decimal(str(stock.get('regularMarketChangePercent', 0.0))) 
                except Exception as e:
                    print(f"Erro de conversão para o símbolo {simbolo}: {e}")
                    continue 

                new_items_to_save.append(
                    CARROSSEL(SIMBOLO=simbolo, PRECO=preco, VARIACAO=variacao)
                )
            else:
                # Se falhar para um único ativo, continua para o próximo
                print(f"DIAGNÓSTICO: API da Brapi não retornou dados em 'results' para {symbol}.")
                print(f"Status Code: {response.status_code}")
                
        # Se houver itens válidos (pelo menos um), atualiza o DB
        if new_items_to_save:
            # B. DELETA TODOS os registros antigos do modelo CARROSSEL
            CARROSSEL.objects.all().delete() 
            
            # C. Salva todos os novos objetos de uma vez
            CARROSSEL.objects.bulk_create(new_items_to_save)
            
            # D. Formata o dado para o JsonResponse e Cache
            stock_data = [
                {'symbol': item.SIMBOLO, 'price': str(item.PRECO), 'change_percent': str(item.VARIACAO)}
                for item in new_items_to_save
            ]
            
            # Define o cache com os dados FRESH da API
            cache.set(cache_key, stock_data, CACHE_DURATION) 
            
            print("Dados da API atualizados e salvos no DB.")
            
        else:
             # Se new_items_to_save estiver vazio, levanta uma exceção para cair no fallback
             raise requests.exceptions.RequestException("API retornou dados vazios para todos os ativos.")


    except requests.exceptions.RequestException as e:
        # 3. Em caso de falha da API ou exceção HTTP
        print(f"Falha na requisição da API ou exceção de rede. Usando dados do DB como fallback. Erro: {e}")
        
        # Pega o último dado salvo no DB (FALLBACK)
        ticker_items = CARROSSEL.objects.all() 
        
        stock_data = []
        for item in ticker_items:
            stock_data.append({
                'symbol': item.SIMBOLO,
                'price': str(item.PRECO),
                'change_percent': str(item.VARIACAO),
            })
            
        # Define o cache com os dados de fallback
        cache.set(cache_key, stock_data, CACHE_DURATION) 
        
    # 4. Retorna a resposta JSON
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
    