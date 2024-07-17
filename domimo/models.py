from django.db import models

class Imobil(models.Model):
    title = models.CharField(max_length=200)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    surface = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    favorites = models.ManyToManyField(User, related_name='favorite_apartments', blank=True)

    def __str__(self):
        return self.title


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.apartment.title}"
class ProjectProfile(models.Model):
    project_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name
class Account(models.Model):
    empcode=models.IntegerField()
    user=models.CharField(max_length=100)
    password= models.CharField(max_length=50)
    number=models.IntegerField()
    e_mail=models.EmailField(max_length=254)
    def __str__(self):
        return self.username
    empAuth_objects=models.Manager()