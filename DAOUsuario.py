class DAOUsuario:
    def __init__(self, e_mail, password):
        # Criando o tipo com as informações
        self.b = models.user.objects.create(email=e_mail,
                                                 senha=password)
        self.b.save()   # Salvando objeto no DataBase

    def atualizar(self, e_mail, password):
        self.b.email=e_mail
        self.b.senha=password

        self.b.save()

    def apagar(self):
        self.b.delete()

    @staticmethod
    def listarusuario():
        # Utiliza um método de models para retornar a listagem
        lista_usuario = models.user.objects.all()
        return lista_usuario

    @staticmethod
    def buscausuario(id):
        conteudo = models.user.objects.get(pk=id)
        return conteudo
