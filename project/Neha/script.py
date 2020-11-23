from django.contrib.auth.models import User
from Neha.models import Profile,Tree
# for i in range(1,17):
#     u = User.objects.create(username = "Neha"+str(i),password="project@123")
#     p = Profile.objects.create(user=u,first_name="Neha",last_name="Mishra",phone=12345678,email="mneha2173@gmail.com",pan_card=123)
#     T = Tree.objects.create(parent = p)
#     t = Tree.objects.get(parent__user__username="Neha")
#     t.sub_tree.add(T)
#     t.save()

def check_user(parent_username,child_username):
    parent_tree = Tree.objects.get(parent__user__username = parent_username)
    if parent_tree.sub_tree.filter(parent__user__username = child_username).exists():
        return True
    for tree in parent_tree.sub_tree.all():
        if check_user(tree.parent.user.username,child_username):
            return True
    return False



print(check_user("Neha","Neha4"))