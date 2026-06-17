"""Data models for the `store` app.

The models are intentionally small and explicit to make them easy to understand
and extend. Keep business logic out of models where possible and prefer
service/helpers to simplify unit testing.
"""

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """A sellable product.

    Attributes
    - name: short product title
    - description: long form description
    - price: unit price
    - image: optional URL to an image
    - stock: integer stock available
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Represents a customer's order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    """An item within an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"