from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from Neha.models import *
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_authenticated is False:
        return redirect('login')
    return render(request, 'Neha/dashboard.html')


def add_new(request):
    print(request.POST)
    username = request.POST.get('username')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = username
    if username and email:
        User.objects.create_user(username=username, password=password, email=email)
        return redirect('dash')

    return render(request, 'Neha/add_new.html')



def check_user(parent_username,child_username):
    parent_tree = Tree.objects.get(parent__user__username = parent_username)
    if parent_tree.sub_tree.filter(parent__user__username = child_username).exists() or parent_username == child_username:
        return True
    for tree in parent_tree.sub_tree.all():
        if check_user(tree.parent.user.username,child_username):
            return True
    return False


def tree(request):
    if request.method == "POST":
        data = request.POST['userid']
        if not check_user(request.user.username, data):
            tree = Tree.objects.get(parent__user=request.user)
            return render(request, 'Neha/tree.html', {'tree': tree,'value':data,"message":"No user found"})
        tree = Tree.objects.get(parent__user__username=data)
        return render(request, 'Neha/tree.html', {'tree': tree,'value':data})
    tree = Tree.objects.get(parent__user = request.user)
    return render(request,'Neha/tree.html',{'tree':tree})


def member_list(request):
    members = Profile.objects.all().exclude(user=request.user)
    context = {
        'members':members
    }
    return render(request, 'Neha/all_members.html',context)

