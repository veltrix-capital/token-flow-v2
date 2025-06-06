from django.db import models
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

    def __str__(self):
        return f"{self.brand} ({self.token_name})"


# User model
class User(models.Model):
    address = models.CharField(max_length=255, unique=True)
    private_key = models.CharField(max_length=255)

    def __str__(self):
        return self.address


# Base Event model using django-polymorphic
class Event(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.__class__.__name__} at {self.created_at}"


# Reward Event
class RewardEvent(Event):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"Reward {self.amount} {self.token} to {self.user}"


# Redeem Event
class RedeemEvent(Event):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"Redeem {self.amount} {self.token} by {self.user}"


# Transfer Event
class TransferEvent(Event):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    from_user = models.ForeignKey(User, related_name='transfers_out', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='transfers_in', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"Transfer {self.amount} {self.token} from {self.from_user} to {self.to_user}"


# Swap Event
class SwapEvent(Event):
    from_user = models.ForeignKey(User, related_name='swaps_out', on_delete=models.CASCADE)
    from_token = models.CharField(max_length=100)
    from_amount = models.DecimalField(max_digits=20, decimal_places=8)
    from_business = models.ForeignKey(Business, related_name='swaps_out', on_delete=models.CASCADE)

    to_user = models.ForeignKey(User, related_name='swaps_in', on_delete=models.CASCADE)
    to_token = models.CharField(max_length=100)
    to_amount = models.DecimalField(max_digits=20, decimal_places=8)
    to_business = models.ForeignKey(Business, related_name='swaps_in', on_delete=models.CASCADE)

    def __str__(self):
        return f"Swap {self.from_amount} {self.from_token} from {self.from_user} to {self.to_amount} {self.to_token} for {self.to_user}"
