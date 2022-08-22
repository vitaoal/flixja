@method_decorator(rate_limit(action="manage_email"), name="dispatch")
class TGerirEmail(AjaxCapableProcessFormViewMixin, FormView):
    template_name = "account/email." + app_settings.TEMPLATE_EXTENSION
    form_class = AddEmailForm
    success_url = reverse_lazy("account_email")

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "add_email", self.form_class)

    def dispatch(self, request, *args, **kwargs):
        sync_user_email_addresses(request.user)
        return super(TGerirEmail, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TGerirEmail, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        email_address = form.save(self.request)
        get_adapter(self.request).add_message(
            self.request,
            messages.INFO,
            "account/messages/email_confirmation_sent.txt",
            {"email": form.cleaned_data["email"]},
        )
        signals.email_added.send(
            sender=self.request.user.__class__,
            request=self.request,
            user=self.request.user,
            email_address=email_address,
        )
        return super(TGerirEmail, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        res = None
        if "action_add" in request.POST:
            res = super(TGerirEmail, self).post(request, *args, **kwargs)
        elif request.POST.get("email"):
            if "action_send" in request.POST:
                res = self._action_send(request)
            elif "action_remove" in request.POST:
                res = self._action_remove(request)
            elif "action_primary" in request.POST:
                res = self._action_primary(request)
            res = res or HttpResponseRedirect(self.get_success_url())
            # Given that we bypassed AjaxCapableProcessFormViewMixin,
            # we'll have to call invoke it manually...
            res = _ajax_response(request, res, data=self._get_ajax_data_if())
        else:
            # No email address selected
            res = HttpResponseRedirect(self.success_url)
            res = _ajax_response(request, res, data=self._get_ajax_data_if())
        return res

    def _get_email_address(self, request):
        email = request.POST["email"]
        try:
            return EnderecoEmail.objects.get_for_user(user=request.user, email=email)
        except EnderecoEmail.DoesNotExist:
            pass

    def _action_send(self, request, *args, **kwargs):
        email_address = self._get_email_address(request)
        if email_address:
            send_email_confirmation(
                self.request, request.user, email=email_address.email
            )

    def _action_remove(self, request, *args, **kwargs):
        email_address = self._get_email_address(request)
        if email_address:
            if email_address.primary:
                get_adapter(request).add_message(
                    request,
                    messages.ERROR,
                    "account/messages/cannot_delete_primary_email.txt",
                    {"email": email_address.email},
                )
            else:
                email_address.delete()
                signals.email_removed.send(
                    sender=request.user.__class__,
                    request=request,
                    user=request.user,
                    email_address=email_address,
                )
                get_adapter(request).add_message(
                    request,
                    messages.SUCCESS,
                    "account/messages/email_deleted.txt",
                    {"email": email_address.email},
                )
                return HttpResponseRedirect(self.get_success_url())

    def _action_primary(self, request, *args, **kwargs):
        email_address = self._get_email_address(request)
        if email_address:
            # Not primary=True -- Slightly different variation, don't
            # require verified unless moving from a verified
            # address. Ignore constraint if previous primary email
            # address is not verified.
            if (
                not email_address.verified
                and EnderecoEmail.objects.filter(
                    user=request.user, verified=True
                ).exists()
            ):
                get_adapter(request).add_message(
                    request,
                    messages.ERROR,
                    "account/messages/unverified_primary_email.txt",
                )
            else:
                # Sending the old primary address to the signal
                # adds a db query.
                try:
                    from_email_address = EnderecoEmail.objects.get(
                        user=request.user, primary=True
                    )
                except EnderecoEmail.DoesNotExist:
                    from_email_address = None
                email_address.set_as_primary()
                get_adapter(request).add_message(
                    request,
                    messages.SUCCESS,
                    "account/messages/primary_email_set.txt",
                )
                signals.email_changed.send(
                    sender=request.user.__class__,
                    request=request,
                    user=request.user,
                    from_email_address=from_email_address,
                    to_email_address=email_address,
                )
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ret = super(TGerirEmail, self).get_context_data(**kwargs)
        # NOTE: For backwards compatibility
        ret["add_email_form"] = ret.get("form")
        # (end NOTE)
        ret["can_add_email"] = EnderecoEmail.objects.can_add_email(self.request.user)
        return ret

    def get_ajax_data(self):
        data = []
        for emailaddress in self.request.user.emailaddress_set.all():
            data.append(
                {
                    "id": emailaddress.pk,
                    "email": emailaddress.email,
                    "verified": emailaddress.verified,
                    "primary": emailaddress.primary,
                }
            )
        return data