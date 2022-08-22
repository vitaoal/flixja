class EnderecoEmail(models.Model):
    """Classe definidora do modelo Usuário, derivada de Model."""
    # Não há necessidade de fazer um método construtor, irá apenas reescrever o __init__ do model

    # Define uma relação de vários para 1 com usuario
    usuario = models.ForeignKey(
        usuario,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=app_settings.UNIQUE_EMAIL,
        max_length=app_settings.EMAIL_MAX_LENGTH,
        verbose_name=_("e-mail address"),
    )
    verified = models.BooleanField(verbose_name=_("verified"), default=False)
    primary = models.BooleanField(verbose_name=_("primary"), default=False)

    def __str__(self):
        return self.email

    def set_as_primary(self, conditional=False):
        old_primary = EnderecoEmail.objects.get_primary(self.usuario)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        usuario_email(self.usuario, self.email)
        self.usuario.save()
        return True