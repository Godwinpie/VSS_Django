# Generated by Django 5.0.4 on 2024-09-15 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_alter_shopsalesorder_customer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shopsalesorder",
            name="typo3_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesorder",
            name="typo3_user_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesorder",
            name="typo3_user_id_sync",
        ),
        migrations.RemoveField(
            model_name="shopsalesorderitem",
            name="typo3_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesorderitem",
            name="typo3_sales_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesorderitem",
            name="typo3_user_id",
        ),
        migrations.RemoveField(
            model_name="shopsalesorderitem",
            name="typo3_user_id_sync",
        ),
    ]
