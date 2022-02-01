# from email import message_from_binary_file, message_from_bytes, message_from_file, message_from_string
# from tkinter import message
from email import message
from django.contrib.messages.api import MessageFailure, error
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from login_page import settings
from django.core.mail import message, send_mail
from django.contrib import messages
# from django import forms



# Create your views here.
 
def home(request):
     return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pass1 = request.POST['pass1']


        #validation of emial)(if email already created then it will not create same user)
        if User.objects.filter(username=username):
            message.error(request, "username already exist, please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            message.error(request, "Email id already exist, please try another email id")
            return redirect('home')
        
        if len(username)>10:
            message.error(request, "Username must be 10 character only")

        if password == pass1:
            message.error(request, "password didn't match!")

        #if username is alphanumeric

        if not username.isalnum():
            message.error(request, "username must be alpha-numeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)

        
        # myuser = forms.save()
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        message.success(request, "Your account has been successfully created....")

        #Welcome Email

        subject = "Welcome to SK Login Portal - Django Login!"
        messages = "Hello" + myuser.first_name + "!! \n" + "Welcome to SK Login Portal \n Thanku for visiting our website \n we have also sent you a confirmation email address order to activate your account. \n\n Thanking You\n Santosh Kumar Govind"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')
        # return HttpResponseRedirect(request.POST.get('signin'))


    return render(request, "authentication/signup.html")


def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})

        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    message.success(request,"you are successfully logout")
    return redirect('home')
    # return render(request, "authentication/signout.html")
    