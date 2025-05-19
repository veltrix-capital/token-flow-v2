import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from analytics.models import Business, User, RewardEvent, RedeemEvent, TransferEvent, SwapEvent

EVENT_TYPE_MAP = {
    'reward': RewardEvent,
    'redeem': RedeemEvent,
    'transfer': TransferEvent,
    'swap': SwapEvent,
}

class Command(BaseCommand):
    help = "Seed the database from data.json"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'analytics', 'fixtures', 'seed.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

        businesses = data.get('businesses', [])
        users = data.get('users', [])
        events = data.get('events', [])

        for item in businesses:
            business = Business.objects.create(
                reward_router=item["rewardRouter"],
                redeem_router=item["redeemRouter"],
                owner=item["owner"],
                private_key=item["privateKey"],
                brand=item["brand"],
                token_name=item["tokenName"],
                token_price=item["tokenPrice"],
            )

            if business:
                self.stdout.write(self.style.SUCCESS(f"Created business: {business.brand}"))

        for item in users:
            user = User.objects.create(
                address=item["address"],
                private_key=item["private_key"],
            )

            if user:
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.address}"))

        for item in events:
            event_type = item.get('type', '').lower()
            ModelClass = EVENT_TYPE_MAP.get(event_type)

            if not ModelClass:
                self.stderr.write(self.style.WARNING(f"Unknown event type '{event_type}', skipping."))
                continue

            if event_type == 'reward':
                event = ModelClass.objects.create(
                    business=item['business'],
                    user=item['user'],
                    amount=item['amount'],
                    token=item['token']
                )
            elif event_type == 'redeem':
                event = ModelClass.objects.create(
                    business=item['business'],
                    user=item['user'],
                    amount=item['amount'],
                    token=item['token']
                )
            elif event_type == 'transfer':
                event = ModelClass.objects.create(
                    business=item['business'],
                    token=item['token'],
                    from_address=item['from'],
                    to_address=item['to'],
                    amount=item['amount']
                )
            elif event_type == 'swap':
                event = ModelClass.objects.create(
                    from_user=item['fromUser'],
                    from_token=item['fromToken'],
                    from_business=item['fromBusiness'],
                    from_amount=item['fromAmount'],
                    to_user=item['toUser'],
                    to_token=item['toToken'],
                    to_business=item['toBusiness'],
                    to_amount=item['toAmount']
                )

            if event:
                self.stdout.write(self.style.SUCCESS(f"Created {event_type} event with ID {event.id}"))
