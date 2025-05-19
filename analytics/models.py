from django.db import models
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

# Business model
class Business(models.Model):
    token = models.CharField(max_length=255)
    reward_router = models.CharField(max_length=255)
    redeem_router = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    token_name = models.CharField(max_length=255)
    token_price = models.DecimalField(max_digits=20, decimal_places=4)

# User model
class User(models.Model):
    address = models.CharField(max_length=255, unique=True)
    private_key = models.CharField(max_length=255)

# Event models
class Event(PolymorphicModel):
    """Base class for all events."""
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__} at {self.created_at}"

class RewardEvent(Event):
    type = models.CharField(max_length=10, default='reward')
    business = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    token = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=8)


class RedeemEvent(Event):
    type = models.CharField(max_length=10, default='redeem')
    business = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    token = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=8)


class TransferEvent(Event):
    type = models.CharField(max_length=10, default='transfer')
    business = models.CharField(max_length=255)
    token = models.CharField(max_length=100)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=8)


class SwapEvent(Event):
    type = models.CharField(max_length=10, default='swap')
    from_user = models.CharField(max_length=255)
    from_token = models.CharField(max_length=100)
    from_amount = models.DecimalField(max_digits=20, decimal_places=8)
    from_business = models.CharField(max_length=255)

    to_user = models.CharField(max_length=255)
    to_token = models.CharField(max_length=100)
    to_amount = models.DecimalField(max_digits=20, decimal_places=8)
    to_business = models.CharField(max_length=255)
