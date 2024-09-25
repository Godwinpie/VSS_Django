from vss.base_erp_importer import BaseImporter
from apps.subscription.models import Subscription  # Adjust the import if the model path differs
from apps.users.models import Customer  # Import the Customer model


class SubscriptionImporter(BaseImporter):
    def fetch_data(self, from_datetime=None):
        # Set up parameters for the request
        params = {
            'Action': 'GetSubscription',
            'fromdatetime': self.get_from_datetime(from_datetime)  # Converts datetime to the expected format
        }
        # Send the request and return the "Subscription" list from the response
        return self.request(params).get("Subscription", [])

    def import_subscription_data(self, subscription_data):
        # Process each subscription record from the fetched data
        for subscription in subscription_data:
            # Fetch or set the customer instance based on 'CustomerID'
            customer_id = subscription.get('CustomerID')
            try:
                customer = Customer.objects.get(customer_number=customer_id)
            except Customer.DoesNotExist:
                yield None, False, f"Customer with customer_number {customer_id} does not exist."
                continue

            # Map the data fields from the subscription to the Subscription model
            subscription_obj, created = Subscription.objects.update_or_create(
                subscription_nr=subscription.get('SubscriptionNr'),
                defaults={
                    'customer': customer,
                    'subscription_code': subscription.get('SubscriptionCode'),
                    'subscription_type': subscription.get('SubscriptionType'),
                    'date_start': subscription.get('DateStart'),
                    'date_end': subscription.get('DateEnd'),
                    'runtime_start': subscription.get('RuntimeStart'),
                    'runtime_end': subscription.get('RuntimeEnd'),
                    'free_of_charge': bool(int(subscription.get('FreeOfCharge', '0'))),
                    'read_only': bool(int(subscription.get('ReadOnly', '0'))),
                    'active': bool(int(subscription.get('Active', '1'))),
                }
            )
            # Yield the result of the operation
            yield subscription_obj, created, None

# Example usage:
# Create an instance of the importer and run the data import
# importer = SubscriptionImporter()
# data = importer.fetch_data()
# for obj, created, error in importer.import_subscription_data(data):
#     if error:
#         print(f"Error: {error}")
#     else:
#         print(f"Subscription {'created' if created else 'updated'}: {obj}")
