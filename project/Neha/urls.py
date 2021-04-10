from django.urls import path,include
from .views import *
urlpatterns = [
    path('', dashboard, name='dash'),
    path('add-new', add_new, name='add_new'),
    path('add-autopool',add_auto_pool,name='add_auto_pool'),
    path('auto-tree/',autopooltree,name='autopooltree'),
    path('tree/',tree,name="tree"),
    path('all_members/',member_list, name="list"),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit-profile'),
    path('update_profile/<int:id>', admin_edit_profile, name='update-profile'),
    path('change_password/<int:id>', change_password, name='change-password'),
    path('add-member/<int:id>',add_member, name='add-member'),
    path('delete-member/<int:id>',delete_member,name='delete-member')
]