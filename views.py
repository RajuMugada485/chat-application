from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import User,Group,Conversation,Message
from genericpath import exists
from django.contrib import messages
from django.contrib.auth import logout
import re
# Create your views here.
def hello(request):
    text="<h1>Hello world</h1>"
    return HttpResponse(text)
def signup(request):
    if request.method=='POST':
        name=(request.POST['first_name']+" "+request.POST['last_name'])
        user_name=request.POST['user_name']
        mail=request.POST['mail']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        secret_key=request.POST['secret']
        try:
            int(user_name)
            messages.info(request,"Username cannot be integer!")
        except:
            pass
        if User.objects.filter(user_name=user_name).exists():
            messages.info(request,"username already existe")
            return redirect('signup')
        if User.objects.filter(mail=mail).exists():
            messages.info(request,"email already exists")
            return redirect('signup')
        if password!=confirm_password:
            messages.info(request,"Both passwords must match")
            return redirect('signup')
        if len(password)<6:
            messages.info(request,"passwords is too small")
            return redirect('signup')
        elif len(password)>15:
            messages.info(request,"password is too large")
            return redirect('signup')
        elif not re.search("[a-z]",password):
            messages.info(request,"It must contain one small letter")
            return redirect('signup')
        elif not re.search("[A-Z]",password):
            messages.info(request,"password must contain atleast One Capital letter")
            return redirect('signup')
        elif not re.search("[0-9]",password):
            messages.info(request,"Password must contain atleast one digit")
            return redirect('signup')
        if len(secret_key)>4:
            messages.info(request,"Secret key Must be less than 3 character")
        u=User.objects.create(user_name=user_name,name=name,mail=mail,password=password,secret=secret_key)
        u.save()
        return redirect('login')
    else:
        return render(request,'signup.html')
def login(request):
    if request.method=='POST':
        login_id=request.POST['login_id']
        password=request.POST['password']
        if not re.search("[@]",login_id):
            if not User.objects.filter(user_name=login_id,password=password).exists():
                messages.info(request,"Invalid Credentials!!")
                return redirect('login')
        elif not User.objects.filter(mail=login_id,password=password).exists():
            messages.info(request,"Invalid Credentials")
            return redirect('login')
        return redirect('contacts',login_id)
    else:
        return render(request,'login.html')
def logout(request):
    return redirect('login')
def contacts(request,user_name):
    if request.method=='POST':
        pass
    else:
        u_id=User.objects.filter(user_name=user_name).values_list('id',flat=True).first()
        con_ids=[i for i in Group.objects.filter(user_id=u_id).values_list('conversation_id',flat=True)]
        user_map=dict()
        for con_id in con_ids:
            user_map[con_id]=[Group.objects.filter(conversation_id=con_id,user_id=u_id).first().conversation_name,Message.objects.filter(conversation_id=con_id).orderby('-sent_datetime').first().text]
        return render(request,'contacts.html',{'user_name':user_name,'conversations':user_map})

def chat(request):
    return render(request,'chatarea.html')
def forgot(request):
    if request.method=='POST':
        login_id=request.POST['login_id']
        secret=request.POST['secret']
        if not User.objects.filter(user_name=login_id,secret=secret).exists():
            messages.info(request,"Invalid credientisals!!")
            return redirect('forgot')
        return redirect('setpwd',login_id)
    else:
        return render(request,'forgot.html')
def setpwd(request,user_name):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password!=confirm_password:
            messages.info(request,"Both password Must match")
            return redirect('setpwd',user_name)
        else:
            u=User.objects.create(user_name=user_name,password=password)
            u.save()
        return redirect('login')
    else:
        return render(request,'setpwd.html')
def search(request,user_name,search_text):
    user_map=dict()
    user_names=[i for i in User.objects.filter(user_name_contains=search_text).exclude(user_name=user_name).values_list('user_name',flat=True)]
    for u_name in user_names:
        user_map[u_name]=[u_name,User.objects.filter(user_name=u_name).values_list('name',flat=True)[0]]

    return render(request,'contacts.html',{"user_name":user_name,"conversations":user_map,"input_text":search_text})
