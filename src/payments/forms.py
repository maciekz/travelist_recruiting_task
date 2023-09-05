from django import forms

from payments.constants import BALANCE_UPDATE_REASONS


class UserBalanceUpdateForm(forms.Form):
    balance_change = forms.IntegerField(required=True)
    balance_update_reason = forms.ChoiceField(choices=BALANCE_UPDATE_REASONS)
