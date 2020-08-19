from django.contrib import admin
from .models import *

class AdminOrder(admin.ModelAdmin):
    list_display = ['user_id','ordered','address']

admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CardItem)
admin.site.register(Order,AdminOrder)
admin.site.register(Address)
