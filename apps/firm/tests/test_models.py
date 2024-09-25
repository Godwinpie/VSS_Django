from django.test import TestCase
from apps.firm.models import Firm, FirmPerson
from apps.users.models import Customer

class FirmModelTest(TestCase):

    def setUp(self):
        # Create a Person instance
        self.person = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

        # Create a Firm instance
        self.firm = Firm.objects.create(
            firm_no='FIRM001',
            name='Test Firm',
            name2='Test Firm Secondary',
            name3='Test Firm Tertiary',
            address='123 Main St',
            address2='Suite 100',
            postal_code='12345',
            city='Test City',
            post_box='PO Box 678',
            postal_code_post_box='67890',
            city_post_box='Post City',
            email_z='contact@testfirm.com',
            phone_z='123-456-7890',
            fax_z='098-765-4321',
            language_code='EN',
            country_code='US',
            advertising=True,
            newsletter=True,
            active=True,
            login_user='testuser',
            login_password='password123',
            web_customer_id='WEB123',
            customer_no='CUST001',
            customer_price_group='PRICE1',
            deb_discount_group='DISCOUNT1',
            invoice_discount_code='INVDISC',
            vat='20',
            payment_method_code='PAYMENT1',
            payment_terms_code='TERMS1',
            vat_reg_number='VAT123',
            membership='MEMBER1',
            access_member_area=True,
            access_personal=True
        )

    def test_create_firm(self):
        # Check that the firm was created correctly
        self.assertEqual(Firm.objects.count(), 1)
        self.assertEqual(self.firm.firm_no, 'FIRM001')
        self.assertEqual(self.firm.name, 'Test Firm')
        self.assertEqual(self.firm.email_z, 'contact@testfirm.com')
        self.assertTrue(self.firm.advertising)
        self.assertTrue(self.firm.access_member_area)
        self.assertEqual(str(self.firm), 'FIRM001 - Test Firm')

    def test_update_firm(self):
        # Update the firm
        self.firm.name = 'Updated Firm Name'
        self.firm.save()
        self.firm.refresh_from_db()
        self.assertEqual(self.firm.name, 'Updated Firm Name')

    def test_delete_firm(self):
        # Delete the firm
        self.firm.delete()
        self.assertEqual(Firm.objects.count(), 0)


class FirmPersonModelTest(TestCase):

    def setUp(self):
        # Create a Person instance
        self.person = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )

        # Create a Firm instance
        self.firm = Firm.objects.create(
            firm_no='FIRM002',
            name='Another Test Firm',
            address='456 Another St',
            postal_code='54321',
            city='Another City',
            email_z='contact@anothertestfirm.com',
            login_user='anotheruser',
            login_password='password456',
            customer_no='CUST002'
        )

        # Create a FirmPerson instance
        self.firm_person = FirmPerson.objects.create(
            firm=self.firm,
            person=self.person
        )

    def test_create_firm_person(self):
        # Check that the FirmPerson was created correctly
        self.assertEqual(FirmPerson.objects.count(), 1)
        self.assertEqual(self.firm_person.firm, self.firm)
        self.assertEqual(self.firm_person.person, self.person)
        self.assertEqual(str(self.firm_person), 'FIRM002 Jane Smith <jane.smith@example.com>')

    def test_update_firm_person(self):
        # Update the FirmPerson's firm
        new_firm = Firm.objects.create(
            firm_no='FIRM003',
            name='New Test Firm',
            address='789 New St',
            postal_code='67890',
            city='New City',
            email_z='contact@newtestfirm.com',
            login_user='newuser',
            login_password='password789',
            customer_no='CUST003'
        )
        self.firm_person.firm = new_firm
        self.firm_person.save()
        self.firm_person.refresh_from_db()
        self.assertEqual(self.firm_person.firm, new_firm)

    def test_delete_firm_person(self):
        # Delete the FirmPerson
        self.firm_person.delete()
        self.assertEqual(FirmPerson.objects.count(), 0)
