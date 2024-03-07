from django.db import models
from django.utils import timezone
from rest_framework.serializers import ValidationError

class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class OrderModel(models.Model):
    start =  models.DateTimeField() # auto_now_add=True
    end = models.DateTimeField()
    total_price = models.IntegerField(blank=True, null=True)

    #product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product')

class OrderedProduct(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='order_products')
    order_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration = models.IntegerField()

    class Meta:
        unique_together = ('order', 'product')


    def clean(self):
        order_start = self.order.start
        order_end = self.order.end

        overlapping_products = OrderedProduct.objects.filter(
            product__name=self.product.name,
            order__end__gte=order_start,
            order__start__lte=order_end
        ).exclude(id=self.id)

        if overlapping_products.exists():
            raise ValidationError('Products with the same name cannot be intersected in time.')

    def save(self, *args, **kwargs):
        self.clean()
        super(OrderedProduct, self).save(*args, **kwargs)