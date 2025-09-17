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
        db_table = 'PROJ1_1_0_CARD2'  # usa exatamente o nome no Oracle

    def __str__(self):
        return self.TITULO
    

    from django.db import models

class CARROSSEL(models.Model):
    SIMBOLO = models.CharField(max_length=10)
    PRECO = models.DecimalField(max_digits=10, decimal_places=2)
    VARIACAO = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'PROJ1_1_0_CARROSSEL'

    def __str__(self):
        return self.SIMBOLO