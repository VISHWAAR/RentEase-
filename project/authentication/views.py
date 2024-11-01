from django.shortcuts import render, redirect,reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages



# Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect(request.build_absolute_uri(reverse('home')))  
        else:
            return HttpResponse("Error")
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect(request.build_absolute_uri(reverse('home')))  
            else:
                messages.error(request, "Form submission failed. Please correct the errors and try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect(request.build_absolute_uri(reverse('login')))  
