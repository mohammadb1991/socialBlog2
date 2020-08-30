from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserLoginFrom,UserRegisteritionForm,EditProfileUser,PhoneLoginForm,CodeLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from posts.models import post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from.models import profilee , Relation
from django.http import JsonResponse




def user_login(request):
    next=request.GET.get('next')
    if request.method=='POST':
        form=UserLoginFrom(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request ,'you logged in successfully','success')
                if next:
                    return redirect(next)
                return redirect('posts:all_posts')
            else:
                messages.error(request ,'some thing went wrong','warning')


    else:
        form=UserLoginFrom()
    return render(request,'account/login.html',{'form':form})

def user_register(request):
    if request.method=='POST':
        form=UserRegisteritionForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.create_user(cd['username'],cd['email'],cd['password'])
            login(request,user)
            messages.success(request,'you register successfully','success')
            return redirect('posts:all_posts')
    else:
        form=UserRegisteritionForm()
    return render(request,'account/register.html',{'form':form})
@login_required
def log_out(request):
    logout(request)
    messages.success(request,'you loged out successfully','success')
    return redirect('posts:all_posts')


@login_required
def user_dashboard(request,userid):
    user=get_object_or_404(User,id=userid)
    posts=post.objects.filter(user=user)
    self_dash=False
    relation=Relation.objects.filter(from_user=request.user , to_user=user)
    if request.user.id == userid:
        self_dash=True
    return render(request, 'account/dashboard.html',{'user':user,'posts':posts,'self_dash':self_dash,'relation':relation})

@login_required
def edit_profile(request,userid):
    user=get_object_or_404(User,pk=userid)
    if request.method=='POST':
        form=EditProfileUser(request.POST,instance=user.profilee)
        if form.is_valid():
            form.save()
            user.email=form.cleaned_data['email']
            user.first_name=form.cleaned_data['fname']
            user.last_name=form.cleaned_data['lname']
            user.save()
            messages.success(request,'you change your profile successfully','success')
            return redirect('account:dashboard',userid)
    else:
        form=EditProfileUser(instance=user.profilee,initial={'email':user.email,'fname':user.first_name,'lname':user.first_name})
    return render(request,'account/edit_profile.html',{'form':form})



def phone_login(request):
    if request.method=='POST':
        form=PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone,rund_num
            phone= f"0{form.cleaned_data['phone']}"
            rund_num=randint(1000,9999)
            api = KavenegarAPI('74306E516B4E7A745157506F562B48666B5058754B744676424A2B416877326873332B70517252442F31553D')
            params = {'sender': '', 'receptor': phone, 'message': rund_num}
            api.sms_send(params)
            return redirect('account:verify')
    else:
        form=PhoneLoginForm()
    return render(request,'account/phone_login.html',{'form':form})

def verify(request):
    if request.method=='POST':
        profile=get_object_or_404(profilee,phone=phone)
        user=get_object_or_404(User, id=profile.user_id)
        form=CodeLoginForm(request.POST)
        if form.is_valid():
            if round_num==form.cleaned_data['code']:
                login(request,user)
                messages.success(request,'you loged in successfully','success')
                return redirect('posts:all_posts')
            else:
                messages.error(request,'verify code is wrong','warning')
    else:
        form=CodeLoginForm()
    return render(request,'account/verify.html',{'form':form})

def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        follow=get_object_or_404(User,pk=user_id)
        check_relation=Relation.objects.filter(from_user=request.user,to_user=follow)
        if check_relation.exists():
            return  JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=follow).save()
            return JsonResponse({'status': 'ok'})

def unfollow(request):
    if request.method=='POST':
        user_id=request.POST['user_id']
        follow=get_object_or_404(User,pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=follow)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'not_exists'})



# Create your views here.

