from django.db import models

# Create your models here.
class Defaulters(models.Model):
    name = models.CharField(max_length=100)
    defaulter_id = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
