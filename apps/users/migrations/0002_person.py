# Generated by Django 5.0.4 on 2024-09-11 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("membership", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("person_no", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("firstname", models.CharField(max_length=255)),
                ("lastname", models.CharField(max_length=255)),
                ("name2", models.CharField(blank=True, max_length=255, null=True)),
                ("name3", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(max_length=255)),
                ("address2", models.CharField(blank=True, max_length=255, null=True)),
                ("postal_code", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=100)),
                ("post_box", models.CharField(blank=True, max_length=255, null=True)),
                ("postal_code_post_box", models.CharField(blank=True, max_length=20, null=True)),
                ("city_post_box", models.CharField(blank=True, max_length=100, null=True)),
                ("email_p", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone_p", models.CharField(blank=True, max_length=50, null=True)),
                ("mobile_p", models.CharField(blank=True, max_length=50, null=True)),
                ("fax_p", models.CharField(blank=True, max_length=50, null=True)),
                ("contact_salutation", models.CharField(blank=True, max_length=10, null=True)),
                ("contact_title", models.CharField(blank=True, max_length=255, null=True)),
                ("language_code", models.CharField(blank=True, max_length=10, null=True)),
                ("country_code", models.CharField(blank=True, max_length=10, null=True)),
                ("advertising", models.BooleanField(default=False)),
                ("occupation", models.CharField(blank=True, max_length=255, null=True)),
                ("newsletter", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                ("typo3_id", models.CharField(blank=True, max_length=50, null=True)),
                ("typo3_user_id", models.CharField(blank=True, max_length=50, null=True)),
                ("typo3_user_id_sync", models.CharField(blank=True, max_length=50, null=True)),
                ("magazine_suv", models.BooleanField(default=False)),
                ("student_status", models.CharField(blank=True, max_length=255, null=True)),
                ("student_id_url", models.URLField(blank=True, null=True)),
                ("student_id_valid_until", models.DateField(blank=True, null=True)),
                ("login_user", models.CharField(blank=True, max_length=255, null=True)),
                ("login_password", models.CharField(blank=True, max_length=255, null=True)),
                ("web_customer_id", models.CharField(blank=True, max_length=255, null=True)),
                ("customer_number", models.CharField(max_length=50, unique=True)),
                ("customer_price_group", models.CharField(blank=True, max_length=50, null=True)),
                ("deb_discount_group", models.CharField(blank=True, max_length=50, null=True)),
                ("invoice_discount_code", models.CharField(blank=True, max_length=50, null=True)),
                ("vat", models.CharField(blank=True, max_length=10, null=True)),
                ("payment_method_code", models.CharField(blank=True, max_length=50, null=True)),
                ("payment_terms_code", models.CharField(blank=True, max_length=50, null=True)),
                ("vat_reg_number", models.CharField(blank=True, max_length=50, null=True)),
                ("firm_no", models.CharField(max_length=50, unique=True)),
                ("access_member_area", models.BooleanField(default=False)),
                ("access_personal", models.BooleanField(default=False)),
                (
                    "member",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="membership.membership"
                    ),
                ),
            ],
            options={
                "db_table": "person",
            },
        ),
    ]
