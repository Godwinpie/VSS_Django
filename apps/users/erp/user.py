import  logging
from apps.users.models import Customer
from apps.membership.models import Membership
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from vss.base_erp_importer import BaseImporter

logger = logging.getLogger(__name__)

def get_person(personno):
    customerImporter = CustomerImporter()
    person_data = customerImporter.fetch_customer_data(personno=personno)
    first_person = customerImporter.get_first_row(person_data)
    if first_person:
        customer_object, created, error_message = customerImporter.process_single_customer(first_person)
        if error_message:
            logger.error(error_message)
        if created:
            logger.info(f'New customer with customer_number: "{personno}". is created.')
            return customer_object
    return None
def get_customer(personno):
    return get_person(personno)

class CustomerImporter(BaseImporter):

    def fetch_customer_data(self, from_datetime=None, personno=None):
        params = {'Action': 'GetCustomer'}
        # Add parameters conditionally based on their presence
        if personno:
            params = {
                'Action': 'GetPerson',
                'personno': personno
            }
            return self.request(params).get("Person", [])
        if from_datetime:
            params = {
                'Action': 'GetCustomer',
                'fromdatetime': self.get_from_datetime(from_datetime)
            }
            return self.request(params).get("Customer", [])

    def import_customers(self, customers_data):
        """Import customer data into the Customer model."""
        for data in customers_data:
            customer_obj, created, error = self.process_single_customer(data)
            yield customer_obj, created, error

    def process_single_customer(self, data):
        """Process a single customer entry and import it into the Customer model."""
        email = data.get('Email', '').strip()
        #if not email:
        #    email = data.get('LoginUser', '').strip()

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return None, data.get('CustomerNumber'), f'Invalid email format: "{email}". Skipping customer.'

        if not email:  # Skip if email is empty
            return None, data.get('CustomerNumber'), 'Email is empty. Skipping customer.'

        # Handle membership
        membership = None
        membership_name = data.get('Membership')
        if membership_name:
            membership, created = Membership.objects.get_or_create(name=membership_name)
        first_name, last_name = self.split_name(data.get('Name', ''))

        defaults = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'customer_number': data.get('CustomerNumber'),
            'name': data.get('Name', ''),
            'name2': data.get('Name2', ''),
            'address': data.get('Address', ''),
            'address2': data.get('Address2', ''),
            'postal_code': data.get('PostalCode', ''),
            'city': data.get('City', ''),
            'contact': data.get('Contact', ''),
            'phone': data.get('Phone', ''),
            'credit_limit': self.parse_decimal(data.get('CreditLimit')),
            'customer_price_group': data.get('CustomerPriceGroup', ''),
            'deb_discount_group': data.get('DebDiscountGroup', ''),
            'invoice_discount_code': data.get('InvoiceDiscountCode', ''),
            'vat': data.get('VAT', ''),
            'interest_condition_code': data.get('InterestConditionCode', ''),
            'currency_code': data.get('CurrencyCode', ''),
            'language_code': data.get('LanguageCode', ''),
            'country_code': data.get('CountryCode', ''),
            'quantity_discount_allowed': bool(int(data.get('QuantityDiscountAllowed', '0'))),
            'reserved_1': data.get('Reserved_1', ''),
            'reserved_2': data.get('Reserved_2', ''),
            'company_ref': data.get('CompanyRef', ''),
            'reserved_3': self.parse_decimal(data.get('Reserved_3')),
            'reserved_4': self.parse_decimal(data.get('Reserved_4')),
            'show_postal_charge': bool(int(data.get('ShowPostalCharge', '0'))),
            'price_includes_vat': bool(int(data.get('PriceIncludesVAT', '0'))),
            'name3': data.get('Name3', ''),
            'name4': data.get('Name4', ''),
            'post_box': data.get('PostBox', ''),
            'postal_code_post_box': data.get('PostalCodePostBox', ''),
            'city_post_box': data.get('CityPostBox', ''),
            'contact_salutation': data.get('ContactSalutation', ''),
            'contact_title': data.get('ContactTitle', ''),
            'fax': data.get('Fax', ''),
            'advertising': bool(int(data.get('Advertisting', '0'))),
            'occupation': data.get('Occupation', ''),
            'vat_reg_number': data.get('VATRegNumber', ''),
            'web_shop_id': data.get('WebShopID', ''),
            'login_name': data.get('LoginName', ''),
            'web_shop_password': data.get('WebShopPassword', ''),
            'type': data.get('Type', 'Person'),
            'access_member_area': bool(int(data.get('AccessMemberArea', '0'))),
            'access_personal': bool(int(data.get('AccessPersonal', '0'))),
            'newsletter': bool(int(data.get('Newsletter', '0'))),
            'active': bool(int(data.get('Active', '1'))),
            'reminder_date': self.parse_date(data.get('ReminderDate')),
            'member': membership,
            'expiry_date': self.parse_date(data.get('ExpiryDate')),
            'student_id_url': data.get('studentIdURL', ''),
            'student_id_valid_until': self.parse_date(data.get('studentIdValidUntil')),
            'student_status': data.get('studentStatus', ''),
        }

        try:
            with transaction.atomic():
                customer_obj, created = Customer.objects.update_or_create(
                    username=email,
                    defaults=defaults,
                )

                # If created, set the password; otherwise, do not change the existing password.
                if created:
                    password = data.get('WebShopPassword', '').strip()
                    if password:
                        customer_obj.set_password(password)
                        customer_obj.save(update_fields=['password'])

                return customer_obj, created, None

        except IntegrityError as e:
            return None, data.get('CustomerNumber'), f'Error saving customer: {str(e)}'
