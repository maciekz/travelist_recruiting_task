from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import FormView, ListView

from payments.forms import UserBalanceUpdateForm
from payments.models import UserWithBalance
from payments.services import update_user_balance


class UserList(ListView):
    model = UserWithBalance
    ordering = ["last_name"]
    template_name = "payments/user_list.html"


class UserBalanceUpdateFormView(FormView):
    form_class = UserBalanceUpdateForm
    template_name = "payments/user_balance_update_form.html"

    @cached_property
    def user_with_balance(self):
        return get_object_or_404(UserWithBalance, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(UserBalanceUpdateFormView, self).get_context_data(**kwargs)
        context["user_with_balance"] = self.user_with_balance
        return context

    def form_valid(self, form):
        # Run service function to update the balance
        update_user_balance(self.user_with_balance, form.cleaned_data["balance_change"])
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
