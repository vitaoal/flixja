class TCatalogo(ListView):
    template_name = 'catalogo/catalogo.html'
    model = models.ItemSerie

    @verified_email_required
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TCatalogo, self).get_context_data(**kwargs)
        context['filmes'] = modelsDAO.ItemFilmeDAO.listarfilme()
        context['series'] = modelsDAO.ItemSerieDAO.listarserie()
        return context