from django.db import models
from apps.users.models import Customer  # Import the Customer model

class PersonExpertRight(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        to_field='customer_number',
        db_column='customer_number',
        null=True,
        blank=True
    )
    committee = models.CharField(max_length=50)
    function = models.CharField(max_length=50, blank=True, null=True)
    com_description = models.CharField(max_length=255, blank=True, null=True)
    com_title_de = models.CharField(max_length=255, blank=True, null=True)
    com_title_en = models.CharField(max_length=255, blank=True, null=True)
    com_title_fr = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.customer_number if self.customer else 'No Customer'} - {self.committee}"

    class Meta:
        db_table = 'person_expert_right'
