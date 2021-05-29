from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from core.forms import SignUpForm


# Create your views here.
def index(request):
    return render(request,'home/index.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, passwerd=password)
            login(request, user)
            return redirect('home:index')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})
