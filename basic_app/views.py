from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import UserForm, UserProfileInfoForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save user info directly to database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)
            user.save()

            # setup then save profile
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'register.html', {'registered':registered,
                                             'user_form':user_form,
                                             'profile_form':profile_form,
                                            })

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active!")
        else:
            # Later, log all this instead of consoling it
            print("someone tried to login and failed")
            print(f"username {username} password {password}")
            return HttpResponse("invalid login details supplied")

    else:
        return render(request, 'login.html', {})
