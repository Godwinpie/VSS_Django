import logging
from vss.base_erp_importer import BaseImporter
from apps.users.models import Person
from apps.membership.models import Membership  # Assuming membership is related to Person

logger = logging.getLogger(__name__)

class PersonImporter(BaseImporter):
    def fetch_data(self, from_datetime=None, person_no=None):
        # Set up the parameters for the request
        params = {
            'Action': 'GetPerson',
        }
        if from_datetime:
            params['fromdatetime'] = self.get_from_datetime(from_datetime)  # Convert datetime to the expected format
        if person_no:
            params['personno'] = person_no

        # Send the request and return the "Person" list from the response
        return self.request(params).get("Person", [])

    def import_person_data(self, person_data):
        # Process each person record from the fetched data
        for person in person_data:
            person_obj, created, error = self.process_single_person(person)
            yield person_obj, created, error

    def process_single_person(self, person):
        # Handle membership
        membership = None
        membership_name = person.get('Membership')
        if membership_name:
            membership, created = Membership.objects.get_or_create(name=membership_name)

        # Split full name into first name and last name
        first_name, last_name = self.split_name(person.get('Name', ''))

        # Try to fetch the Customer object if available
        #customer_number = person.get('CustomerNo')
        #customer = None
        #if customer_number:
        #    try:
        #        customer = Customer.objects.get(customer_number=customer_number)
        #    except Customer.DoesNotExist:
        #        logger.info(f"Customer with customer_number {customer_number} does not exist.")

        try:
            # Map the data fields from the person to the Person model
            person_obj, created = Person.objects.update_or_create(
                person_no=person.get('PersonNo'),
                defaults={
                    'name': person.get('Name'),
                    'firstname': first_name,
                    'lastname': last_name,
                    'name2': person.get('Name2', ''),
                    'name3': person.get('Name3', ''),
                    'address': person.get('Address'),
                    'address2': person.get('Address2', ''),
                    'postal_code': person.get('PostalCode'),
                    'city': person.get('City'),
                    'post_box': person.get('PostBox', ''),
                    'postal_code_post_box': person.get('PostalCodePostBox', ''),
                    'city_post_box': person.get('CityPostBox', ''),
                    'email_p': person.get('EmailP'),
                    'phone_p': person.get('PhoneP', ''),
                    'mobile_p': person.get('MobileP', ''),
                    'fax_p': person.get('FaxP', ''),
                    'contact_salutation': person.get('ContactSalutation', ''),
                    'contact_title': person.get('ContactTitle', ''),
                    'language_code': person.get('LanguageCode', ''),
                    'country_code': person.get('CountryCode', ''),
                    'advertising': bool(int(person.get('Advertisting', '0'))),
                    'occupation': person.get('Occupation', ''),
                    'newsletter': bool(int(person.get('Newsletter', '0'))),
                    'active': bool(int(person.get('Active', '1'))),
                    'typo3_id': person.get('TYPO3ID', ''),
                    'typo3_user_id': person.get('TYPO3userID', ''),
                    'typo3_user_id_sync': person.get('TYPO3userIDSync', ''),
                    'magazine_suv': bool(int(person.get('MagazineSUV', '0'))),
                    'student_status': person.get('StudentStatus', ''),
                    'student_id_url': person.get('StudentIdURL', ''),
                    'student_id_valid_until': self.parse_date(person.get('StudentIdValidUntil')),
                    'login_user': person.get('LoginUser', ''),
                    'login_password': person.get('LoginPassword', ''),
                    'web_customer_id': person.get('WebCustomerID', ''),
                    'customer_number': person.get('CustomerNo', ''),
                    'customer_price_group': person.get('CustomerPriceGroup', ''),
                    'deb_discount_group': person.get('DebDiscountGroup', ''),
                    'invoice_discount_code': person.get('InvoiceDiscountCode', ''),
                    'vat': person.get('VAT', ''),
                    'payment_method_code': person.get('PaymentMethodCode', ''),
                    'payment_terms_code': person.get('PaymentTermsCode', ''),
                    'vat_reg_number': person.get('VATRegNumber', ''),
                    #'firm_no': person.get('FirmNo', ''),
                    'member': membership,
                    'access_member_area': bool(int(person.get('AccessMemberArea', '0'))),
                    'access_personal': bool(int(person.get('AccessPersonal', '0')))
                }
            )
            return person_obj, created, None
        except Exception as e:
            logger.error(f"Error processing person: {str(e)}")
            return None, False, str(e)

