from django.core.management.base import BaseCommand
from restaurant_menu.models import Order
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Automatically update order statuses'

    def handle(self, *args, **kwargs):
        orders = Order.objects.filter(status__in=['Pending', 'Confirmed'])
        for order in orders:
            old_status = order.status
            order.update_status()
            new_status = order.status

            if old_status != new_status:
                self.stdout.write(self.style.SUCCESS(f'Order {order.id} status updated from {old_status} to {new_status}'))
                logger.info(f'Order {order.id} status updated from {old_status} to {new_status}')
            else:
                self.stdout.write(self.style.NOTICE(f'Order {order.id} status remains {old_status}'))
                logger.info(f'Order {order.id} status remains {old_status}')
