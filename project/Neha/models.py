from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)



class Tree(models.Model):
    parent = models.ForeignKey(Profile,on_delete = models.CASCADE)
    sub_tree = models.ManyToManyField('self',symmetrical = False)
# Create your models here.
