from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email =models.EmailField(null=True)
    profile_pic = models.ImageField(upload_to='profile', default='default.png',null=True)
    pan_card = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Tree(models.Model):
    parent = models.OneToOneField(Profile, on_delete=models.CASCADE)
    sub_tree = models.ManyToManyField('self', symmetrical=False,blank=True)
    def __str__(self):
        return self.parent.user.username
# Create your models here.
