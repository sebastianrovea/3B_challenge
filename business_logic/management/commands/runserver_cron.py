import time
from django.core.management.base import BaseCommand
from ...jobs.lower_stock import check_stock
from ...utils.const import TIME_CHECK_LOWER_STOCK


class Command(BaseCommand):
    help = 'Check lower stock periodically. Yopu can set this time'

    def handle(self, *args, **options):
        print('Starting cron handle...')
        try:
            while True:
                check_stock()
                time.sleep(TIME_CHECK_LOWER_STOCK)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Deteniendo el cron job simulado...'))
