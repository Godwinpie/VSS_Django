import  logging
from vss.base_erp_importer import BaseImporter
from apps.firm.models import Firm,FirmPerson
from apps.users.models import Customer
from apps.users.erp.user import get_person

logger = logging.getLogger(__name__)

def get_firm(firmno):
    firmImporter = FirmImporter()
    firm_data = firmImporter.fetch_data_firm(firmno=firmno)
    first_firm = firmImporter.get_first_row(firm_data)
    if first_firm:
        firm_object, created, error_message = process_single_firm(first_firm)
        if created:
            return firm_object
    return None

def process_single_firmperson(firmperson):
    try:
        customer = Customer.objects.get(customer_number=firmperson.get('PersonNo'))
    except Customer.DoesNotExist:
        customer = get_person(firmperson.get('PersonNo'))
    if customer is None:
        return None, False, f"Customer with PersonNo {firmperson.get('PersonNo')} does not exist."

    try:
        firm = Firm.objects.get(firm_no=firmperson.get('FirmNo'))
    except Firm.DoesNotExist:
        firm = get_firm(firmperson.get('FirmNo'))
    if firm is None:
        return None, False, f"Firm with FirmNo {firmperson.get('FirmNo')} does not exist."

    try:
        firmperson_obj, created = FirmPerson.objects.update_or_create(
            firm_no=firm,
            person_no=customer,
            defaults={
                'name': firmperson.get('Name'),
                'name2': firmperson.get('Name2', ''),
                'name3': firmperson.get('Name3', ''),
                'contact': firmperson.get('Contact', ''),
                'address': firmperson.get('Address', ''),
                'address2': firmperson.get('Address2', ''),
                'postal_code': firmperson.get('PostalCode', ''),
                'city': firmperson.get('City', ''),
                'post_box': firmperson.get('PostBox', ''),
                'postal_code_post_box': firmperson.get('PostalCodePostBox', ''),
                'city_post_box': firmperson.get('CityPostBox', ''),
                'country_code': firmperson.get('CountryCode', ''),
                'email_g': firmperson.get('EmailG', ''),
                'phone_g': firmperson.get('PhoneG', ''),
                'mobile_g': firmperson.get('MobileG', ''),
                'invoice_to': firmperson.get('InvoiceTo', '0'),
            }
        )
        return firmperson_obj, created, None
    except Firm.DoesNotExist:
        return None, False, f"Firm with FirmNo {firmperson.get('FirmNo')} does not exist."
    except Customer.DoesNotExist:
        return None, False, f"Customer with PersonNo {firmperson.get('PersonNo')} does not exist."
    except Exception as e:
        # Handle any exceptions and return the error
        return None, False, str(e)


def process_single_firm(firm):
    try:
        firm_obj, created = Firm.objects.update_or_create(
            firm_no=firm.get('FirmNo'),
            defaults={
                'name': firm.get('Name'),
                'name2': firm.get('Name2', ''),
                'name3': firm.get('Name3', ''),
                'address': firm.get('Address'),
                'address2': firm.get('Address2', ''),
                'postal_code': firm.get('PostalCode'),
                'city': firm.get('City'),
                'post_box': firm.get('PostBox', ''),
                'postal_code_post_box': firm.get('PostalCodePostBox', ''),
                'city_post_box': firm.get('CityPostBox', ''),
                'email_z': firm.get('EmailZ'),
                'phone_z': firm.get('PhoneZ'),
                'fax_z': firm.get('FaxZ', ''),
                'language_code': firm.get('LanguageCode', ''),
                'country_code': firm.get('CountryCode', ''),
                'advertising': bool(int(firm.get('Advertisting', '0'))),
                'newsletter': bool(int(firm.get('Newsletter', '0'))),
                'active': bool(int(firm.get('Active', '1'))),
                'login_user': firm.get('LoginUser'),
                'login_password': firm.get('LoginPassword'),
                'web_customer_id': firm.get('WebCustomerID', ''),
                'customer_no': firm.get('CustomerNo'),
                'customer_price_group': firm.get('CustomerPriceGroup', ''),
                'deb_discount_group': firm.get('DebDiscountGroup', ''),
                'invoice_discount_code': firm.get('InvoiceDiscountCode', ''),
                'vat': firm.get('VAT'),
                'payment_method_code': firm.get('PaymentMethodCode', ''),
                'payment_terms_code': firm.get('PaymentTermsCode', ''),
                'vat_reg_number': firm.get('VATRegNumber', ''),
                'membership': firm.get('Membership', ''),
                'access_member_area': bool(int(firm.get('AccessMemberArea', '0'))),
                'access_personal': bool(int(firm.get('AccessPersonal', '0'))),
            }
        )
        return firm_obj, created, None
    except Exception as e:
        # Handle any exceptions and return the error
        return None, False, str(e)


class FirmImporter(BaseImporter):
    def fetch_data_firm(self, from_datetime=None, firmno=None):
        params = {'Action': 'GetFirm'}

        # Add parameters conditionally based on their presence
        if firmno:
            params['firmno'] = firmno
        if from_datetime:
            params['fromdatetime'] =  self.get_from_datetime(from_datetime)

        return self.request(params).get("Firm", [])

    def import_firm(self, firm_data):
        # Process each firm
        for firm in firm_data:
            firm_obj, created, error = process_single_firm(firm)
            yield firm_obj, created, error

    def fetch_data_firmperson(self, from_datetime=None, firmno=None):
        params = {
            'Action': 'GetConnection',
            'fromdatetime': self.get_from_datetime(from_datetime)
        }
        return self.request(params).get("ConnectionPersonFirm", [])

    def import_firmperson(self, firmperson_data):
        # Process each firm
        for firmperson in firmperson_data:
            firmperson_obj, created, error = process_single_firmperson(firmperson)
            yield firmperson_obj, created, error

