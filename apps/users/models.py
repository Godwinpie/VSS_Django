import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# from djstripe.models import Customer

from apps.users.helpers import validate_profile_picture
from apps.membership.models import Membership

def _get_avatar_filename(instance, filename):
    """Use random filename prevent overwriting existing files & to fix caching issues."""
    return f'profile-pictures/{uuid.uuid4()}.{filename.split(".")[-1]}'


class Customer(AbstractUser):
    """
    Add additional fields to the user model here.
    """

    customer_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customer_price_group = models.CharField(max_length=50, blank=True, null=True)
    deb_discount_group = models.CharField(max_length=50, blank=True, null=True)  # Increased from 5 to 50
    invoice_discount_code = models.CharField(max_length=50, blank=True, null=True)
    vat = models.CharField(max_length=5, blank=True, null=True)
    interest_condition_code = models.CharField(max_length=50, blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    language_code = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=50, blank=True, null=True)
    quantity_discount_allowed = models.BooleanField(default=False)
    reserved_1 = models.CharField(max_length=50, blank=True, null=True)
    reserved_2 = models.CharField(max_length=50, blank=True, null=True)
    company_ref = models.CharField(max_length=20)
    reserved_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reserved_4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    show_postal_charge = models.BooleanField(default=False)
    price_includes_vat = models.BooleanField(default=False)
    name3 = models.CharField(max_length=255, blank=True, null=True)
    name4 = models.CharField(max_length=255, blank=True, null=True)
    post_box = models.CharField(max_length=255, blank=True, null=True)
    postal_code_post_box = models.CharField(max_length=20, blank=True, null=True)
    city_post_box = models.CharField(max_length=100, blank=True, null=True)
    contact_salutation = models.CharField(max_length=50, blank=True, null=True)  # Increased from 5 to 50
    contact_title = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    advertising = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    vat_reg_number = models.CharField(max_length=50, blank=True, null=True)
    web_shop_id = models.CharField(max_length=255, blank=True, null=True)
    login_name = models.CharField(max_length=255, blank=True, null=True)
    web_shop_password = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, choices=[("Person", "Person"), ("Company", "Company")])
    access_member_area = models.BooleanField(default=False)
    access_personal = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    shop_customer_number = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    reminder_date = models.DateField(null=True, blank=True)
    member = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    student_id_url = models.URLField(blank=True, null=True)
    student_id_valid_until = models.DateField(null=True, blank=True)
    student_status = models.CharField(max_length=255, blank=True, null=True)

    avatar = models.FileField(upload_to=_get_avatar_filename, blank=True, validators=[validate_profile_picture])
    language = models.CharField(max_length=250, blank=True, null=True)
    timezone = models.CharField(max_length=250, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "users_customer"

    def __str__(self):
        return f"{self.get_full_name()} <{self.email or self.username}>"

    def get_display_name(self) -> str:
        if self.get_full_name().strip():
            return self.get_full_name()
        return self.email or self.username

    @property
    def avatar_url(self) -> str:
        if self.avatar:
            return self.avatar.url
        else:
            return "https://www.gravatar.com/avatar/{}?s=128&d=identicon".format(self.gravatar_id)

    @property
    def gravatar_id(self) -> str:
        # https://en.gravatar.com/site/implement/hash/
        return hashlib.md5(self.email.lower().strip().encode("utf-8")).hexdigest()

    def has_firm_vss(user):
        if not user.is_authenticated:
            return False
        return user.firmperson_set.filter(name="VSS").exists()

    def get_membership(self, person):
        if not person.member:
            return
        membership = person.member.name
        membership_choices = {
            "1. EHREN": _("Honorary member"),
            "2. VETERAN": _("Veteran"),
            "3. EINZEL": _("Individual member"),
            "4. INST": _("Corporate member"),
            "5. STUDENT": _("Student member"),
            "6. FREIE": _("Free members"),
            "7. FREIE I": _("Free institutional members"),
        }
        return membership_choices.get(membership)

    def get_magazine_suv(self, person):
        return person.magazine_suv

    @property
    def get_period(self):
        return self.subscription_set.filter(active=True).order_by('-date_end').first()

    @property
    def get_expert_rights(self):
        return self.personexpertright_set.filter(active=True).first()


class Person(models.Model):
    person_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255, blank=True, null=True)
    name3 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    post_box = models.CharField(max_length=255, blank=True, null=True)
    postal_code_post_box = models.CharField(max_length=20, blank=True, null=True)
    city_post_box = models.CharField(max_length=100, blank=True, null=True)
    email_p = models.EmailField(blank=True, null=True)
    phone_p = models.CharField(max_length=50, blank=True, null=True)
    mobile_p = models.CharField(max_length=50, blank=True, null=True)
    fax_p = models.CharField(max_length=50, blank=True, null=True)
    contact_salutation = models.CharField(max_length=10, blank=True, null=True)
    contact_title = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    advertising = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    typo3_id = models.CharField(max_length=50, blank=True, null=True)
    typo3_user_id = models.CharField(max_length=50, blank=True, null=True)
    typo3_user_id_sync = models.CharField(max_length=50, blank=True, null=True)
    magazine_suv = models.IntegerField(blank=True, null=True)
    student_status = models.CharField(max_length=255, blank=True, null=True)
    student_id_url = models.URLField(blank=True, null=True)
    student_id_valid_until = models.DateField(blank=True, null=True)
    login_user = models.CharField(max_length=255, blank=True, null=True)
    login_password = models.CharField(max_length=255, blank=True, null=True)
    web_customer_id = models.CharField(max_length=255, blank=True, null=True)
    customer_number = models.CharField(max_length=50, blank=True, null=True)
    customer_price_group = models.CharField(max_length=50, blank=True, null=True)
    deb_discount_group = models.CharField(max_length=50, blank=True, null=True)
    invoice_discount_code = models.CharField(max_length=50, blank=True, null=True)
    vat = models.CharField(max_length=10, blank=True, null=True)
    payment_method_code = models.CharField(max_length=50, blank=True, null=True)
    payment_terms_code = models.CharField(max_length=50, blank=True, null=True)
    vat_reg_number = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    access_member_area = models.BooleanField(default=False)
    access_personal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.person_no})"

    class Meta:
        db_table = 'person'

class CustomerShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer,
        to_field='customer_number',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Customer'
    )
    delivery_address_code = models.CharField(max_length=20, verbose_name='Delivery Address Code')
    name = models.CharField(max_length=100, verbose_name='Name')
    name2 = models.CharField(max_length=100, blank=True, null=True, verbose_name='Name 2')
    address = models.CharField(max_length=255, verbose_name='Address')
    address2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address 2')
    postal_code = models.CharField(max_length=10, verbose_name='Postal Code')
    city = models.CharField(max_length=100, verbose_name='City')
    country_code = models.CharField(max_length=2, verbose_name='Country Code')
    typo3_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='TYPO3 ID')
    typo3_user_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='TYPO3 User ID')
    typo3_user_id_sync = models.CharField(max_length=20, blank=True, null=True, verbose_name='TYPO3 User ID Sync')

    class Meta:
        db_table = 'customer_shipping_address'
        verbose_name = 'Customer Shipping Address'
        verbose_name_plural = 'Customer Shipping Addresses'

    def __str__(self):
        return f"{self.name} ({self.customer_id})"
