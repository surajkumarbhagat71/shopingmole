from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_tatil = models.CharField(max_length=200)

    def __str__(self):
        return self.cat_tatil


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='media/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.product_name


    def get_totals_price(self):
        return  self.price


    def get_discount_toal_price(self):
        data=(self.get_totals_price() * self.discount_price)/100
        return self.get_totals_price() - data


class CardItem(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orders = models.BooleanField(default=False)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.product_name


    def get_total_price(self):
        return self.qty * self.item.price


    def get_discount_price(self):
        data=(self.get_total_price() * self.item.discount_price)/100
        return self.get_total_price() - data


    def get_save_amount(self):
        return self.get_total_price() - self.get_discount_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_price()
        else:
            return self.get_total_price()



TYPE_CHOICE = {
    ("W","WORK"),
    ("H","HOME"),
}

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    pin = models.IntegerField()
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    landmark = models.CharField(max_length=200)
    alternative_no = models.IntegerField()
    address_type = models.CharField(choices=TYPE_CHOICE, max_length=2)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(CardItem)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)


    def get_total(self):
        total = 0
        for x in self.items.all():
            total += x.get_final_price()
        return total


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    order_id = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username









