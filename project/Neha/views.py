from datetime import datetime, date, timedelta
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from Neha.models import *
from .forms import ProfileForm, PasswordChange
from django.db.models import Count
from django.db import transaction
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_authenticated is False:
        return redirect('login')
    total_members = Profile.objects.all().count()
    print(total_members)
    today = datetime.today()
    last_seven = datetime.now() - timedelta(days=6)
    last_seven_date = last_seven.date()
    newmem_count = Profile.objects.all().filter(created_at__date__range=[last_seven_date,today]).count()
    print(newmem_count)
    your_commission = "Rs.30000"
    revenue = "90%"
    context = {
        'total_mem':total_members,
        'new_mem':newmem_count,
        'rev':revenue,
        'comm':your_commission
    }
    return render(request, 'Neha/dashboard.html',context)

def No_of_child(username,count=0):
    tree = Tree.objects.get(parent__user__username=username)
    count += len(tree.sub_tree.all())
    for t in tree.sub_tree.all():
        count = No_of_child(t.parent.user.username,count)
    return count

@login_required
def add_new(request):
    parent_tree = Tree.objects.get(parent=Profile.objects.get(user=request.user))
    if len(parent_tree.sub_tree.all()) > 20:
        message = 'Already 20 users are added you cannot add more!'
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
        p = Profile.objects.create(user=user, email=email, phone=phone,created_by = request.user)
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
    if not request.user.profile.is_admin:
        return HttpResponse(status=404)
    try:
        p = Profile.objects.get(user=request.user)
    except:
        return HttpResponse(status = 404)
    if request.method == "POST":
        data = request.POST['userid']
        try:
            tree = AutoTree.objects.get(parent__user__username=data)
        except:
            tree = AutoTree.objects.get(parent = p)
            return render(request, 'Neha/tree.html', {'tree': tree, 'value': data, "message": "No user found","auto":True})
        return render(request, 'Neha/tree.html', {'tree': tree,'value':data,"auto":True})
    tree = AutoTree.objects.get(parent = p)
    return render(request, 'Neha/tree.html', {'tree': tree,'len':len(tree.sub_tree.all()),"auto":True})


# @login_required
def check_user(parent_username,child_username):
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
    if request.user.profile.is_admin:
        members = Profile.objects.all().exclude(user=request.user)
        context = {
            'members': members
        }
        return render(request, 'Neha/all_members.html', context)

    members = Profile.objects.filter(soft_delete=False).exclude(user=request.user)    ###[30:40]
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


@login_required
def change_password(request,id):
    if not request.user.profile.is_admin:
        return HttpResponse(status=404)
    new_pass = request.POST.get('new_password1')
    new_pass2 = request.POST.get('new_password2')
    if new_pass != new_pass2:
        messages.warning(request, _('Please Enter Same Password'))
        return redirect(f'../change_password/{id}')
    userr = User.objects.get(id=id)
    print(userr.password)
    if request.method == 'POST':
        userr.set_password(new_pass)
        update_session_auth_hash(request, request.user)
        userr.save()
        print('succe')
        messages.success(request, _(f'password has been successfully updated! of {userr.username}'))
        return redirect('list')
    else:
        form = PasswordChange()
    return render(request, 'Neha/change_password.html', {'form': form})

@login_required
def add_member(request,id):
    if not request.user.profile.is_admin:
        return HttpResponse(status=404)
    if request.method == 'POST':
        parent_user = User.objects.get(id=id)
        if parent_user.profile.soft_delete:
            return HttpResponse(status=404)
        parent_tree = Tree.objects.get(parent=parent_user.profile)
        if len(parent_tree.sub_tree.all()) > 20:
            message = 'Already 20 users are added you cannot add more!'
            context = {'message': message}
            return render(request, 'Neha/add_new.html', context)

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
            p = Profile.objects.create(user=user, email=email, phone=phone, created_by=request.user)
            t = Tree.objects.create(parent=p)
            parent_tree.sub_tree.add(t)
            parent_tree.save()
            child_tree = AutoTree.objects.create(parent=p)
            autotree = AutoTree.objects.annotate(c=Count('sub_tree')).filter(c__lte=2)[0]
            autotree.sub_tree.add(child_tree)
            messages.success(request,f"{username} is added below {parent_user.username}")

            return redirect('list')
    return render(request, 'Neha/add_new.html')

def delete(parent_profile):
    tree = Tree.objects.get(parent=parent_profile)
    parent_profile.soft_delete = True
    parent_profile.save()
    dt,c = DeletedTree.objects.get_or_create(parent=parent_profile)
    for t in tree.sub_tree.all():
        st,c = DeletedTree.objects.get_or_create(parent=t.parent)
        dt.sub_tree.add(st)
        dt.save()
        delete(t.parent)

    # dt.sub_tree.add(*tree.sub_tree.all())
    # dt.save()
    # tree.delete()


@login_required
def delete_member(request,id):
    if not request.user.profile.is_admin:
        return HttpResponse(status=404)
    with transaction.atomic():
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        p = Profile.objects.get(user=user)
        delete(p)
        tree = Tree.objects.get(parent=p)
        # dt = DeletedTree.objects.create(parent=tree.parent)
        # dt.sub_tree.add(*tree.sub_tree.all())
        tree.delete()
    messages.success(request, f"{user.username} deleted successfully")
    return redirect('list')


# sample_memeber3