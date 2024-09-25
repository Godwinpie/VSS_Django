from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, Person, CustomerShippingAddress

# Unregister the model if it's already registered
if Customer in admin.site._registry:
    admin.site.unregister(Customer)

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    # Add or remove fields you want to display in the admin here.
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': (
            'first_name', 'last_name', 'email', 'name', 'name2', 'address', 'address2', 'postal_code', 'city',
            'contact', 'phone', 'avatar', 'student_id_url', 'student_id_valid_until', 'student_status')
        }),
        ('Additional Info', {
            'fields': (
            'customer_number', 'credit_limit', 'customer_price_group', 'deb_discount_group', 'invoice_discount_code',
            'vat', 'interest_condition_code', 'currency_code', 'language_code', 'country_code',
            'quantity_discount_allowed', 'reserved_1', 'reserved_2', 'company_ref', 'reserved_3', 'reserved_4',
            'show_postal_charge', 'price_includes_vat', 'name3', 'name4', 'post_box', 'postal_code_post_box',
            'city_post_box', 'contact_salutation', 'contact_title', 'fax', 'advertising', 'occupation',
            'vat_reg_number', 'web_shop_id', 'login_name', 'web_shop_password', 'type', 'access_member_area',
            'access_personal', 'newsletter', 'shop_customer_number', 'active', 'reminder_date',
            'member', 'expiry_date', 'language', 'timezone')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fields to display in the list view
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_staff', 'customer_number', 'shop_customer_number')

    # Fields to search in the admin search bar
    search_fields = ('id','username', 'email', 'first_name', 'last_name', 'shop_customer_number')

    # Filters to use in the admin sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # Add or remove fields you want to display in the admin here.
    # Fields to display in the list view
    list_display = ('id','name', 'firstname', 'lastname','customer_number', 'email_p')
    # Fields to search in the admin search bar
    search_fields = ('id','name', 'firstname', 'lastname','customer_number')

@admin.register(CustomerShippingAddress)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id','delivery_address_code', 'name', 'address', 'address', 'address2', 'postal_code')
    search_fields = ('name', 'address', 'postal_code', 'city')