class ItemSerie(models.Model):
    """Classe definidora do modelo Série, derivada de Model."""

    # Campos

    item_nome = models.CharField(max_length=150, help_text='Insira o nome da série')
    item_desc = models.CharField(max_length=800, help_text='Insira a descrição da série')
    item_original = models.BooleanField(help_text='Original Flixjá', null=True)
    item_novo = models.BooleanField(help_text='Conteúdo lançamento', null=True)

    # Requer a biblioteca Pillow
    item_thumb = models.ImageField(upload_to='images', null=True)


    # Métodos

    def getName(self):
        """ Retorna uma string nome da serie"""
        return self.item_nome

    def getDesc(self):
        """ Retorna uma string descrição da serie"""
        return self.item_desc

    def __str__(self):
        """ String para representar o objeto MyModelName (no site Admin)."""
        return self.item_nome