from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Gender(models.Model):
    Name = models.CharField(max_length=100)
    def __str__(self):
        return self.Name


class State(models.Model):
    state = models.CharField(max_length=20)
    def __str__(self):
        return self.state


class City(models.Model):
    city = models.CharField(max_length=20)
    def __str__(self):
        return self.city


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender,on_delete=models.SET_NULL,null=True)
    DOB = models.DateTimeField(auto_now_add=True,null=True)
    Address = models.CharField(max_length=30,null=True)
    pin_code = models.CharField(max_length=20,null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email =models.EmailField(null=True)
    profile_pic = models.ImageField(upload_to='profile', default='default.png',null=True)
    pan_card = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    created_by = models.ForeignKey(User,on_delete = models.SET_NULL,null = True,related_name="created_by",blank=True)
    is_admin = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)

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


class DeletedTree(models.Model):
    parent = models.OneToOneField(Profile, on_delete=models.CASCADE)
    sub_tree = models.ManyToManyField('self', symmetrical=False,blank=True)
    def __str__(self):
        return self.parent.user.username

# Create your models here.
