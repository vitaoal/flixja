class TStreaming(ListView):
    template_name = 'detalhes/detalhes.html'
    model = models.ItemSerie

    @verified_email_required
    def get_context_data(self, *, object_list=None, **kwargs):
        tipo = self.request.GET.get('tipo')
        id = self.request.GET.get('id')
        context = super(TStreaming, self).get_context_data(**kwargs)
        if tipo == "0":
            context['conteudo'] = modelsDAO.ItemFilmeDAO.buscafilme(id)
            context['tipo'] = "0"

        elif tipo == "1":
            context['conteudo'] = modelsDAO.ItemSerieDAO.buscaserie(id)
            context['tipo'] = "1"
            context['episodios'] = modelsDAO.ItemEpDAO.listarep()

        elif tipo == "2":
            context['conteudo'] = modelsDAO.ItemEpDAO.buscaep(id)
            context['tipo'] = "2"

        return context