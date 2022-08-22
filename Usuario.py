class Usuario(models.Model):
    """Classe definidora do modelo Usuário, derivada de Model."""
    # Não há necessidade de fazer um método construtor, irá apenas reescrever o __init__ do model

    # Campos
    email = models.CharField(max_length=150)
    item_senha = models.CharField(max_length=150)

    def getName(self):
        """ Retorna uma string nome da serie"""
        return self.item_nome

    def getDesc(self):
        """ Retorna uma string descrição da serie"""
        return self.item_desc