class TAlterarSenha(AjaxCapableProcessFormViewMixin, FormView):
    template_name = "account/password_set." + app_settings.TEMPLATE_EXTENSION
    form_class = SetPasswordForm
    success_url = reverse_lazy("account_set_password")

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "set_password", self.form_class)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.has_usable_password():
            return HttpResponseRedirect(reverse("account_change_password"))
        return super(TAlterarSenha, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return super(TAlterarSenha, self).render_to_response(
            context, **response_kwargs
        )

    def get_form_kwargs(self):
        kwargs = super(TAlterarSenha, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        logout_on_password_change(self.request, form.user)
        get_adapter(self.request).add_message(
            self.request, messages.SUCCESS, "account/messages/password_set.txt"
        )
        signals.password_set.send(
            sender=self.request.user.__class__,
            request=self.request,
            user=self.request.user,
        )
        return super(TAlterarSenha, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(TAlterarSenha, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret["password_set_form"] = ret.get("form")
        # (end NOTE)
        return ret
