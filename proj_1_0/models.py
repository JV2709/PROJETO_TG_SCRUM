from django.db import models

class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text
    


class Card2(models.Model):
    TITULO = models.CharField(max_length=20)
    TEXTO = models.CharField(max_length=300)

    class Meta:
        db_table = 'PROJ1_1_0_CARD2'  

    def __str__(self):
        return self.TITULO
   

class DICIONARIO(models.Model):
    TITULO = models.CharField(max_length=100)
    CATEGORIA = models.CharField(max_length=50)
    TEXTO = models.TextField()  
    IMAGEM = models.CharField(max_length=200, blank=True, null=True) 
    
    class Meta:
        db_table = 'PROJ1_1_0_DICIONARIO'
    
    def __str__(self):
       return self.TITULO




class CARROSSEL(models.Model):
    SIMBOLO = models.CharField(max_length=10)
    PRECO = models.DecimalField(max_digits=10, decimal_places=2)
    VARIACAO = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'PROJ1_1_0_CARROSSEL'

    def __str__(self):
        return self.SIMBOLO
    
class Investimento(models.Model):
    TIPO= [
        ('Renda Fixa', 'Renda Fixa'),
        ('Renda Variável', 'Renda Variável'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO, default='Renda Fixa')
    descricao = models.TextField()
    rentabilidade = models.TextField()
    link_imagem = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Investimento"
        verbose_name_plural = "Investimentos"
        ordering = ['tipo', 'nome']
        
    def __str__(self):
        return self.nome
    
class PerguntaPerfil(models.Model):
    pergunta = models.CharField(max_length=300)
    alternativa_um = models.CharField(max_length=300)
    alternativa_dois = models.CharField(max_length=300)
    alternativa_tres = models.CharField(max_length=300)

    class Meta:
        db_table = 'PROJ1_1_0_PERGUNTA_PERFIL'
        verbose_name = 'Pergunta de Perfil'
        verbose_name_plural = 'Perguntas de Perfil'

    def __str__(self):
        return self.pergunta

