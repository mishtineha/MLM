from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from Neha.models import *
from .forms import ProfileForm
from django.db.models import Count
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_authenticated is False:
        return redirect('login')
    return render(request, 'Neha/dashboard.html')

def No_of_child(username,count=0):
    tree = Tree.objects.get(parent__user__username=username)
    count += len(tree.sub_tree.all())
    for t in tree.sub_tree.all():
        count = No_of_child(t.parent.user.username,count)
    return count

@login_required
def add_new(request):
    if No_of_child(request.user.username) > 12:
        message = 'Already 12 users are added you cannot add more!'
        context = {'message': message}
        return render(request, 'Neha/add_new.html', context)


    username = request.POST.get('username')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = username
    if User.objects.filter(username=username).exists():
        message = 'This Username already exists, please choose another one! '
        context = {'message':message}
        return render(request, 'Neha/add_new.html', context)
    if username and email:
        user = User.objects.create_user(username=username, password=password, email=email)
        p = Profile.objects.create(user=user, email=email, phone=phone)
        t= Tree.objects.create(parent=p)
        parent_tree = Tree.objects.get(parent = Profile.objects.get(user = request.user))
        parent_tree.sub_tree.add(t)
        parent_tree.save()
        child_tree =  AutoTree.objects.create(parent = p)
        autotree = AutoTree.objects.annotate(c = Count('sub_tree')).filter(c__lte = 2)[0]
        autotree.sub_tree.add(child_tree)

        return redirect('dash')

    return render(request, 'Neha/add_new.html')

@login_required
def add_auto_pool(request):
    p = Profile.objects.get(user=request.user)
    username = request.POST.get('username')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = username
    if User.objects.filter(username=username).exists():
        message = 'This Username already exists, please choose another one! '
        context = {'message': message}
        return render(request, 'Neha/add_new.html', context)
    if username and email:
        user = User.objects.create_user(username=username, password=password, email=email)
        AutoPool_Profile.objects.create(user=user, email=email, phone=phone,created_by=p)

        return redirect('dash')

    return render(request, 'Neha/add_new.html')

# def get_mem(profiles,parent_tree):
#     for p in profiles:
#         autotree,c = AutoTree.objects.get_or_create(parent = p)
#             if len(parent_tree.sub_tree.all()) < 3:
#                 parent_tree.sub_tree.add(autotree)
#
#

@login_required
def autopooltree(request):
    try:
        p = Profile.objects.get(user=request.user)
    except:
        return HttpResponse(status = 404)
    tree = AutoTree.objects.get(parent = p)
    return render(request, 'Neha/tree.html', {'tree': tree,'len':len(tree.sub_tree.all())})


# @login_required
def check_user(parent_username,child_username):
    print("CHild username")
    print(child_username)
    parent_tree = Tree.objects.get(parent__user__username = parent_username)
    if parent_tree.sub_tree.filter(parent__user__username = child_username).exists() or parent_username == child_username:
        return True
    for tree in parent_tree.sub_tree.all():
        if check_user(tree.parent.user.username,child_username):
            return True
    return False


@login_required
def tree(request):
    if request.method == "POST":
        data = request.POST['userid']
        if not check_user(request.user.username, data):
            tree = Tree.objects.get(parent__user=request.user)
            return render(request, 'Neha/tree.html', {'tree': tree,'value':data,"message":"No user found"})
        tree = Tree.objects.get(parent__user__username=data)
        return render(request, 'Neha/tree.html', {'tree': tree,'value':data})
    tree = Tree.objects.get(parent__user = request.user)
    return render(request,'Neha/tree.html',{'tree':tree,'len':len(tree.sub_tree.all())})


@login_required
def member_list(request):
    members = Profile.objects.all().exclude(user=request.user)[30:40]
    mem = []
    for m in members:
        if check_user(request.user.username,m.user.username):
            mem.append(m)

    context = {
        'members':mem
    }
    return render(request, 'Neha/all_members.html',context)


@login_required
def profile(request):
    member = Profile.objects.filter(user=request.user)[0]
    context = {
        'member':member
    }
    return render(request, 'Neha/Profile.html',context)


@login_required
def edit_profile(request):
    member = Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=member)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            print('save')
    form = ProfileForm(instance=member)
    context = {
        'form':form,
        'member':member
    }
    return render(request, 'Neha/edit_profile.html',context)


@login_required
def admin_edit_profile(request,id):
    member = Profile.objects.get(id=id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance = member)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            print('save')
    form = ProfileForm(instance=member)
    context = {
        'form':form,
        'member':member
    }
    return render(request, 'Neha/admin_edit_profile.html',context)