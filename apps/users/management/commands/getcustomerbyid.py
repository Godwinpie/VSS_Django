from django.core.management.base import BaseCommand
from apps.users.erp.user import get_customer
import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'Fetch customer data from a third-party API and insert it into the database'

    def add_arguments(self, parser):
        parser.add_argument('--personno', type=str,
                            help='get customer by personno')

    def handle(self, *args, **kwargs):

        personno = kwargs.get('personno')
        customer_data = get_customer(personno=personno)
        logger.log(customer_data)

        #for customer_obj, created, error_message in get_customer(personno=personno):
        #    self.stdout.write(self.style.ERROR(customer_obj))
        #    if error_message:
        #        self.stdout.write(self.style.ERROR(error_message))
        #    elif created:
        #        self.stdout.write(self.style.SUCCESS(f'Created new customer: {customer_obj.username}'))
        #    else:
        #        self.stdout.write(self.style.SUCCESS(f'Updated existing customer: {customer_obj.username}'))

        self.stdout.write(self.style.SUCCESS('Customer data import completed successfully.'))
