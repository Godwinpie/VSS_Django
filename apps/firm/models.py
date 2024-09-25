from django.db import models
from  apps.users.models import Customer

class Firm(models.Model):
    firm_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255, blank=True, null=True)
    name3 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    post_box = models.CharField(max_length=255, blank=True, null=True)
    postal_code_post_box = models.CharField(max_length=20, blank=True, null=True)
    city_post_box = models.CharField(max_length=100, blank=True, null=True)
    email_z = models.EmailField()
    phone_z = models.CharField(max_length=50, blank=True, null=True)
    fax_z = models.CharField(max_length=50, blank=True, null=True)
    language_code = models.CharField(max_length=5, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    advertising = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    login_user = models.CharField(max_length=255)
    login_password = models.CharField(max_length=255)
    web_customer_id = models.CharField(max_length=20, blank=True, null=True)
    customer_no = models.CharField(max_length=20)
    customer_price_group = models.CharField(max_length=50, blank=True, null=True)
    deb_discount_group = models.CharField(max_length=50, blank=True, null=True)
    invoice_discount_code = models.CharField(max_length=50, blank=True, null=True)
    vat = models.CharField(max_length=5, blank=True, null=True)
    payment_method_code = models.CharField(max_length=50, blank=True, null=True)
    payment_terms_code = models.CharField(max_length=50, blank=True, null=True)
    vat_reg_number = models.CharField(max_length=50, blank=True, null=True)
    membership = models.CharField(max_length=50, blank=True, null=True)
    access_member_area = models.BooleanField(default=False)
    access_personal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firm_no} - {self.name}"
    class Meta:
        db_table = "firm"

class FirmPerson(models.Model):
    firm_no = models.ForeignKey(Firm, to_field='firm_no', on_delete=models.CASCADE, verbose_name="Firm Number", null=True, blank=True)
    person_no = models.ForeignKey(Customer, to_field='customer_number', on_delete=models.CASCADE, verbose_name="Person Number", null=True, blank=True)
    #firm_no = models.CharField(max_length=10, verbose_name="Firm Number", null=True, blank=True)
    #person_no = models.CharField(max_length=10, verbose_name="Person Number", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Name", blank=True, null=True)
    name2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name 2")
    name3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name 3")
    contact = models.CharField(max_length=255, blank=True, null=True, verbose_name="Contact")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    address2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address 2")
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Postal Code")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    post_box = models.CharField(max_length=100, blank=True, null=True, verbose_name="Post Box")
    postal_code_post_box = models.CharField(max_length=10, blank=True, null=True, verbose_name="Postal Code Post Box")
    city_post_box = models.CharField(max_length=100, blank=True, null=True, verbose_name="City Post Box")
    country_code = models.CharField(max_length=2, blank=True, null=True, verbose_name="Country Code")
    email_g = models.EmailField(max_length=255, blank=True, null=True, verbose_name="General Email")
    phone_g = models.CharField(max_length=20, blank=True, null=True, verbose_name="General Phone")
    mobile_g = models.CharField(max_length=20, blank=True, null=True, verbose_name="General Mobile")
    invoice_to = models.CharField(max_length=10, blank=True, null=True, verbose_name="Invoice To")

    class Meta:
        db_table = 'firm_person'

    def __str__(self):
        return f"{self.name} ({self.person_no})"
