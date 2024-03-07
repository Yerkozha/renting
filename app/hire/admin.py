from django.contrib import admin

# Register your models here.


from .models import ProductModel, OrderedProduct, OrderModel

@admin.register(ProductModel)
class ProductModel(admin.ModelAdmin):

    list_display = ('name', 'price', )


# @admin.register(OrderModel)
# class OrderModel(admin.ModelAdmin):
#
#     list_display = ('order', 'product', 'order_price', 'duration', )
#
@admin.register(OrderedProduct)
class OrderedProduct(admin.ModelAdmin):

    list_display = ('order', 'order_price', 'duration', 'product', )