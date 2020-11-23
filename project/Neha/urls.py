from django.urls import path,include
from .views import *
urlpatterns = [
    path('', dashboard, name='dash'),
    path('add-new', add_new, name='add_new'),
    path('tree/',tree,name="tree"),
]