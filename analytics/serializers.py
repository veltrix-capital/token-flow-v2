# analytics/serializers.py
from drf_polymorphic.serializers import PolymorphicSerializer

from rest_framework import serializers
from .models import (
    Business, User,
    Event, RewardEvent, RedeemEvent,
    TransferEvent, SwapEvent
)

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

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

class EventPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        RewardEvent: RewardEventSerializer,
        RedeemEvent: RedeemEventSerializer,
        TransferEvent: TransferEventSerializer,
        SwapEvent: SwapEventSerializer,
    }
