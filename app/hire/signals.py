from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderedProduct


@receiver(post_save, sender=OrderedProduct)
def my_handler(sender, instance, created, **kwargs):

    if not instance.order_price:
        instance.order_price = instance.product.price * instance.duration
        print("instance.order_price", instance.order_price)
        instance.save()
