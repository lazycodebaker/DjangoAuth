from django.http.response import HttpResponse, HttpResponseBadRequest
from .models import UserModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render

from django.conf import settings
from django.contrib.auth  import authenticate, login , logout
from django.core.mail import send_mail

@csrf_exempt
def Home(request):
    context = {
        "request" : request,        
    }
    user_id = request.COOKIES.get('user_id')
    if user_id:
        profile = UserModel.objects.filter(id=user_id).first()
        
        if profile:
            user = profile.user
            login(request,user=user)
    
    return render(request,"home.html",context=context)

    

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"login.html")

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"register.html")


@csrf_exempt
def Register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":

        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']  
        confirm_password = request.POST['confirm_password']   

        try:
            if password == confirm_password:

                if User.objects.filter(username=username).first():
                    return HttpResponse("User already Registered")
                
                elif User.objects.filter(email=email).first():
                    return HttpResponse("User already Registered")            

                else:
                    user = User.objects.create_user(username=username,email=email)
                    user.set_password(password)
                    user.first_name = firstName
                    user.last_name = lastName                
                    user.save()

                    UserModel.save()

                    return  redirect('home')
            else:
                return HttpResponse("unmatched passwords ")

        except Exception as e:
            return HttpResponse(e)

    else:
        return HttpResponseBadRequest("Bad Request")


@csrf_exempt
def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    user_id = request.COOKIES.get('user_id')

    if user_id:
        user = User.objects.filter(id=user_id).first()

        if user:
            login(request,user=user)

        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        email = str(request.POST['email'])
        password = str(request.POST['password'])

        user = User.objects.filter(email=email).first()

        if user:
            if(user.check_password(password) and (user.username == username) and (user.email == email)):
                profile = UserModel.objects.filter(user=user).first()
                if profile:                     
                    authenticate(email=email,password=password)
                    login(request,user=user)
                    response =  redirect("home")
                    response.set_cookie("user_id",str(profile.id))

                    return response
                else:
                    return HttpResponse("NO user profile found please register first .")
            else:
                return HttpResponse("invalid credentials")
        else:
            return HttpResponse("user not found")

    else:
        return HttpResponse("re-login please")
    

@csrf_exempt
@login_required
def Logout(request):  

    if request.method == 'POST':
        logout(request)
        response = redirect('home')
        response.delete_cookie("user_id")
             
        return response
    else:
        return HttpResponseBadRequest("bad request .")    
