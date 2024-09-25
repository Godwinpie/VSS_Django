from vss.base_erp_importer import BaseImporter
from apps.users.models import CustomerShippingAddress
from apps.users.models import Customer
from apps.users.erp.user import get_customer# Assuming the Customer model is in apps.customer.models


def process_single_shipping_address(shipping_address):
    try:
        # Attempt to get the Customer object; set to None if it does not exist
        customer_id = shipping_address.get('CustomerID')
        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(customer_number=customer_id)
            except Customer.DoesNotExist:
                customer = get_customer(customer_id)
                if not customer:
                    return None, None, f'Customer with ID {customer_id} not found. Skipping Customer address import.'

        # Process CustomerShippingAddress
        shipping_address_obj, created = CustomerShippingAddress.objects.update_or_create(
            delivery_address_code=shipping_address.get('DeliveryAddressCode'),
            defaults={
                'customer': customer,
                'name': shipping_address.get('Name'),
                'name2': shipping_address.get('Name2', ''),
                'address': shipping_address.get('Address'),
                'address2': shipping_address.get('Address2', ''),
                'postal_code': shipping_address.get('PostalCode'),
                'city': shipping_address.get('City'),
                'country_code': shipping_address.get('CountryCode'),
                'typo3_id': shipping_address.get('TYPO3ID', ''),
                'typo3_user_id': shipping_address.get('TYPO3userID', ''),
                'typo3_user_id_sync': shipping_address.get('TYPO3userIDSync', ''),
            }
        )
        return shipping_address_obj, created, None
    except Exception as e:
        # Handle any exceptions and return the error
        return None, False, str(e)


class CustomerShippingAddressImporter(BaseImporter):

    def fetch_data(self, from_datetime=None, customer_no=None):
        # Set up the parameters for the request
        params = {
            'Action': 'GetShipToAdr',
        }
        if from_datetime:
            params['fromdatetime'] = self.get_from_datetime(from_datetime)  # Convert datetime to the expected format
        if customer_no:
            params['customerno'] = customer_no

        return self.request(params).get("ShipmentAddress", [])

    def import_shipping_addresses(self, shipping_address_data):
        # Process each shipping address
        for shipping_address in shipping_address_data:
            shipping_address_obj, created, error = process_single_shipping_address(shipping_address)
            yield shipping_address_obj, created, error
