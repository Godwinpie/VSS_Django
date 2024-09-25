import logging
from vss.base_erp_importer import BaseImporter
from apps.gremien.models import PersonExpertRight
from apps.users.models import Customer
from apps.users.erp.user import get_person

logger = logging.getLogger(__name__)

class PersonExpertRightImporter(BaseImporter):
    def fetch_data(self, from_datetime=None):
        # Define the API request parameters
        params = {
            'Action': 'GetExpertRights',
            'fromdatetime': self.get_from_datetime(from_datetime)  # Converts datetime to the expected format
        }
        # Send the request and return the "ExpertRights" list from the response
        return self.request(params).get("ExpertRights", [])

    def import_expert_rights_data(self, expert_rights_data):
        # Process each expert right record from the fetched data
        for expert_right in expert_rights_data:
            expert_right_obj, created, error = self.process_single_expert_right(expert_right)
            yield expert_right_obj, created, error

    def process_single_expert_right(self, expert_right):
        # Try to fetch the customer by CustomerNumber
        customer_number = expert_right.get('CustomerNumber')
        customer = None
        if customer_number:
            try:
                customer = Customer.objects.get(customer_number=customer_number)
            except Customer.DoesNotExist:
                customer = get_person(customer_number)  # Attempt to retrieve customer using the helper method

        # Log and handle the case when the customer does not exist
        if not customer:
            logger.error(f"Customer with CustomerNumber {customer_number} does not exist.")
            return None, False, f"Customer with CustomerNumber {customer_number} does not exist."

        # Process and create/update the expert right record
        try:
            expert_right_obj, created = PersonExpertRight.objects.update_or_create(
                customer=customer,
                committee=expert_right.get('Committee'),
                defaults={
                    'function': expert_right.get('Function', ''),
                    'com_description': expert_right.get('ComDescription', ''),
                    'com_title_de': expert_right.get('ComTitleDE', ''),
                    'com_title_en': expert_right.get('ComTitleEN', ''),
                    'com_title_fr': expert_right.get('ComTitlefr', ''),
                    'active': bool(int(expert_right.get('Active', '0'))),
                }
            )
            return expert_right_obj, created, None
        except Exception as e:
            logger.error(f"Error processing expert right: {str(e)}")
            return None, False, str(e)
