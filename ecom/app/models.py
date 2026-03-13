from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomManager(models.Manager):
    def get_price_range(self,r1,r2):
        return self.filter(price__range=(r1,r2))
    def get_dairyproduct_list(self):
        return self.filter(category__exact="Dairyproduct")
    def get_meatproduct_list(self):
        return self.filter(category__exact="Meat Product")
    def get_organicfood_list(self):
        return self.filter(category__exact="Organic Food")
    def get_fruits_list(self):
        return self.filter(category__exact="Fruits")

class Product(models.Model):
    cat = ( ('Dairyproduct', 'Dairyproduct'), 
        ('Meat Product', 'Meat Product'), 
        ('Organic Food', 'Organic Food'), 
        ('Fruits', 'Fruits'))
    userid = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,choices=cat,default="")
    desc = models.TextField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_img")
    objects = models.Manager()
    prod = CustomManager()
    
    def __str__(self):
        return self.product_name

    @property
    def nutrition_info(self):
        if self.desc:
            from .utils import analyze_food_description
            return analyze_food_description(self.desc)
        return "No description available"
    
    
class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,)
    qty = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories_per_100g = models.FloatField()
    protein_per_100g = models.FloatField()
    carbs_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()

    def __str__(self):
        return self.name