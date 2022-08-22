class ItemFilme(models.Model):
    """Classe definidora do modelo Filme, derivada de Model."""
    # Não há necessidade de fazer um método construtor, irá apenas reescrever o __init__ do model

    # Campos

    item_nome= models.CharField(max_length=150, help_text='Insira o nome do filme')
    item_desc = models.CharField(max_length=800, help_text='Insira a descrição do filme')
    item_original = models.BooleanField(help_text='Original Flixjá', null=True)
    item_novo = models.BooleanField(help_text='Conteúdo lançamento', null=True)
    item_thumb = models.ImageField(upload_to ='images', null=True) # Requer a biblioteca Pillow
    item_video = models.FileField(upload_to='videos', blank=True, null=True)

    # Métodos
    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.item_nome

    def getName(self):
        """ Retorna uma string nome do filme"""
        return self.item_nome

    def getDesc(self):
        """ Retorna uma string descrição do filme"""
        return self.item_desc