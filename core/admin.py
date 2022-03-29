from django.contrib import admin
from core.models import MenuItem, Tag, Category, Order, OrderedItem, Payment

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Payment)
