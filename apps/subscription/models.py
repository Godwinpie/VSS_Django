from django.db import models
from apps.users.models import Customer  # Import the Customer model

class Subscription(models.Model):
    SUBSCRIPTION_CODE_ALLOWED='VSS DIGI'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, to_field='customer_number',
                                 db_column='customer_number')
    subscription_nr = models.CharField(max_length=50, unique=True)
    subscription_code = models.CharField(max_length=50)
    subscription_type = models.CharField(max_length=1, choices=[("D", "Digital"), ("P", "Print")])
    date_start = models.DateField()
    date_end = models.DateField()
    runtime_start = models.DateField()
    runtime_end = models.DateField()
    free_of_charge = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subscription_nr} - {self.subscription_code}"
    class Meta:
        db_table = 'subscription'