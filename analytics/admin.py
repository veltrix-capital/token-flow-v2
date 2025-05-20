from django.contrib import admin
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter
)

from .models import (
    Event,
    RewardEvent,
    RedeemEvent,
    TransferEvent,
    SwapEvent,
    Business,
    User
)

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('brand', 'token', 'token_name', 'token_price')
    search_fields = ('brand', 'token')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('address', )
    search_fields = ('address', )

@admin.register(RewardEvent)
class RewardEventAdmin(PolymorphicChildModelAdmin):
    base_model = RewardEvent
    show_in_index = True
    list_display = ('id', 'business', 'user', 'amount', 'created_at')


@admin.register(RedeemEvent)
class RedeemEventAdmin(PolymorphicChildModelAdmin):
    base_model = RedeemEvent
    show_in_index = True
    list_display = ('id', 'business', 'user', 'amount', 'created_at')


@admin.register(TransferEvent)
class TransferEventAdmin(PolymorphicChildModelAdmin):
    base_model = TransferEvent
    show_in_index = True
    list_display = ('id', 'business', 'from_address', 'to_address', 'amount', 'created_at')


@admin.register(SwapEvent)
class SwapEventAdmin(PolymorphicChildModelAdmin):
    base_model = SwapEvent
    show_in_index = True
    list_display = ('id', 'from_user', 'to_user', 'from_amount', 'to_amount', 'created_at')


@admin.register(Event)
class EventAdmin(PolymorphicParentModelAdmin):
    base_model = Event
    child_models = (RewardEvent, RedeemEvent, TransferEvent, SwapEvent)
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('id', 'polymorphic_ctype', 'created_at')
