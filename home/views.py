from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#import re
from home.EmailBackEnd import EmailBackEnd
# Create your views here.

def index(request):
    return render(request,'home/index.html')

def home(request):
    return render(request,'home/home.html')
def test(request):
    return render(request,'home/test.html')
def dgp(request):
    return render(request,'dgp.html')

def handleLogin(request):
    if request.method !='POST':
        return HttpResponse('Submission outside this window is not allowed 😎')
    else:
        #Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user =EmailBackEnd.authenticate(request, username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfuly logged in 🥰")
            user_type = user.user_type
            #print("username : "+ request.POST.get("loginusername")+ "Password: " +request.POST.get("loginpassword"))
            if user_type == '1':
                return redirect('admin_home')
            #elif user_type == '2':
                # return HttpResponse("Staff Login")
                #return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
        else:
            messages.error(request, "Invalid credentialsl, Please try again 😎")
            return redirect('index')
    
    
def handleLogout(request):
    if request.method=='POST':
        value=request.POST['value']
        logout(request)
        messages.success(request, "Successfuly logged out 🥰")
        return redirect('index')
    else:
        return HttpResponse('Sorry No Users Logged in 😎')    