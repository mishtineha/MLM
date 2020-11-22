from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.IntegerField()
    email =models.EmailField(null=True)
    profile_pic = models.ImageField(upload_to='profile', default='default.png')
    pan_card = models.IntegerField()

    def __str__(self):
        return self.first_name


def post_save_member(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance, email=instance.email)
        except:
            pass


post_save.connect(post_save_member, sender=User)

class Tree(models.Model):
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sub_tree = models.ManyToManyField('self', symmetrical=False)
# Create your models here.
