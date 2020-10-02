from django.db import models

# Create your models here.
class Post(models.Model):
    email = models.CharField(max_length=254)
    vec = models.IntegerField()


