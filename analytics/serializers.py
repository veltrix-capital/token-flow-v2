# analytics/serializers.py
from rest_framework import serializers
from .models import (
    Business, User,
    Event, RewardEvent, RedeemEvent,
    TransferEvent, SwapEvent
)

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'id',
            'token',
            'reward_router',
            'redeem_router',
            'owner',
            'brand',
            'token_name',
            'token_price'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'address']

class RewardEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardEvent
        fields = '__all__'

class RedeemEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedeemEvent
        fields = '__all__'

class TransferEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferEvent
        fields = '__all__'

class SwapEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwapEvent
        fields = '__all__'

class EventSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if isinstance(instance, RewardEvent):
            return RewardEventSerializer(instance).data
        elif isinstance(instance, RedeemEvent):
            return RedeemEventSerializer(instance).data
        elif isinstance(instance, TransferEvent):
            return TransferEventSerializer(instance).data
        elif isinstance(instance, SwapEvent):
            return SwapEventSerializer(instance).data
        else:
            return super().to_representation(instance)
