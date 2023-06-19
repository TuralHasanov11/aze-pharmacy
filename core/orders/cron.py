import logging
import os
from datetime import datetime, timedelta

from orders.models import Order

logger = logging.getLogger('cron')


def delete_expired_orders():
    end_date = datetime.today().date() - timedelta(days=int(os.environ.get('ORDER_EXPIRY_DAYS', 7))) 
    Order.objects.filter(payment_status=Order.PaymentStatus.PENDING, created_at__lte=end_date).delete()
    logger.info(f"Orders expired at {end_date} were deleted!")