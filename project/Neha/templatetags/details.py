from Neha.models import *
from django import template
register = template.Library()

@register.filter
def calculate_commission(username,com=100,sum=0):
    tree = Tree.objects.get(parent__user__username = username)

    if tree.sub_tree.all().count() == 0:
        com = com * 2

        return sum
    for t in tree.sub_tree.all():
        sum = sum + com
    com = com/2
    for t in tree.sub_tree.all():
        sum = calculate_commission(t.parent.user.username,com,sum)
    return sum

@register.filter
def No_of_child(username,count=0):
    tree = Tree.objects.get(parent__user__username=username)
    count += len(tree.sub_tree.all())
    for t in tree.sub_tree.all():
        count = No_of_child(t.parent.user.username,count)
    return count

@register.filter
def parent_id(username):
    tree = Tree.objects.get(parent__user__username=username)
    try:
        parent_tree = Tree.objects.get(sub_tree = tree)
        return parent_tree.parent.user.username
    except Exception as e:
        print("===============================")
        print(e)
        return username