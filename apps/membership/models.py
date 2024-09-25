from django.db import models

class Membership(models.Model):
    name = models.CharField(max_length=50)  # The name of the membership level or type

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'membership'