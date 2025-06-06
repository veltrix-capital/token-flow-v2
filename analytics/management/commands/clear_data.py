from django.core.management.base import BaseCommand
from analytics.models import Business, User, Event, RewardEvent, RedeemEvent, TransferEvent, SwapEvent

class Command(BaseCommand):
    help = "Delete all records from Business, User and Event models"

    def handle(self, *args, **kwargs):
        event_count = Event.objects.count()

        RewardEvent.objects.all().delete()
        RedeemEvent.objects.all().delete()
        TransferEvent.objects.all().delete()
        SwapEvent.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {event_count} Event records."))

        business_count = Business.objects.count()
        Business.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {business_count} Business records."))

        user_count = User.objects.count()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {user_count} User records."))
