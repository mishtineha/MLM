from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Tree)
admin.site.register(AutoTree)
admin.site.register(Gender)
admin.site.register(City)
admin.site.register(State)
admin.site.register(DeletedTree)