from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['requestpassword']

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            
            except:
                error_message = "Error while creating your account!"
                return render(request, 'signup.html', {'error_message': error_message})
            
        else:
            error_message = 'Password donot match!'
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')

def user_logout(request):
    pass
