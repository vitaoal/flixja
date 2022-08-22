class ItemEp(models.Model):
    # ForeignKey: Define uma relação de vários para um (Many-to-one) com série
    post = models.ForeignKey(ItemSerie, default=None, on_delete=models.CASCADE)
    item_nome = models.CharField(max_length=150, help_text='Insira o nome do episódio', null=True)
    item_desc = models.CharField(max_length=800, help_text='Insira a descrição do episódio', null=True)
    item_n_ep = models.IntegerField(null=True, help_text='Insira o número do episódio')
    item_video = models.FileField(upload_to='videos', blank=True, null=True)

    def __str__(self):
        return self.item_nome