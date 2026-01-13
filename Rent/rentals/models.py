from django.db import models
from inventory.models import Cloth


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Rental(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rent_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20)

    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refundable_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Rental #{self.id}"


class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.rental.id} - {self.cloth.name}"
