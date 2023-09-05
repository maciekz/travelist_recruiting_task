from django.db.models import F

from payments.models import UserWithBalance


def some_additional_function_to_run_on_balance_update():
    pass


def update_user_balance(
    user_with_balance: UserWithBalance,
    balance_change: int,
    run_additional_function: bool = True,
):
    user_with_balance.balance = F("balance") + balance_change
    user_with_balance.save()
    if run_additional_function:
        some_additional_function_to_run_on_balance_update()
