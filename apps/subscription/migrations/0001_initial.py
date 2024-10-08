# Generated by Django 5.0.4 on 2024-08-29 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subscription_nr", models.CharField(max_length=50, unique=True)),
                ("subscription_code", models.CharField(max_length=50)),
                ("subscription_type", models.CharField(choices=[("D", "Digital"), ("P", "Print")], max_length=1)),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("runtime_start", models.DateField()),
                ("runtime_end", models.DateField()),
                ("free_of_charge", models.BooleanField(default=False)),
                ("read_only", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=True)),
                (
                    "customer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "db_table": "subscription",
            },
        ),
    ]
