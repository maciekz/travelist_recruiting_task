import factory


class UserWithBalanceFactory(factory.django.DjangoModelFactory):
    """UserWithBalance factory."""

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    balance = factory.Faker("random_int")

    class Meta:
        model = "payments.UserWithBalance"
