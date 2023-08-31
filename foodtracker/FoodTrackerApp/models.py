from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse



# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


### add food items ###
class Food(models.Model):
    food_name = models.CharField(max_length=200, )
    quantity = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    calories = models.IntegerField(default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=7, decimal_places=2)
    protein = models.DecimalField(max_digits=7, decimal_places=2)
    food_img = models.ImageField(blank=True, upload_to='food_img')
    info = models.CharField(max_length=2000, default="Test data goes here")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("food_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.food_name



