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
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name="created_by")
    is_admin = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


class AutoPool_Profile(models.Model):
    created_by = models.ForeignKey(Profile,on_delete = models.SET_NULL,null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(upload_to='profile', default='default.png', null=True)
    pan_card = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Tree(models.Model):
    parent = models.OneToOneField(Profile, on_delete=models.CASCADE)
    sub_tree = models.ManyToManyField('self', symmetrical=False,blank=True)
    def __str__(self):
        return self.parent.user.username


class AutoTree(models.Model):
    parent = models.OneToOneField(Profile, on_delete=models.CASCADE)
    sub_tree = models.ManyToManyField('self', symmetrical=False,blank=True)
    def __str__(self):
        return self.parent.user.username
# Create your models here.
