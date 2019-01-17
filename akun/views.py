from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm

# Create your views here.
def signup(request):
    #return render(request, 'signupAkun.html')
    #form = UserCreationForm()
    #return render(request, 'signupAkun.html', {'form': form})
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        #form = UserCreationForm()
        form = SignUpForm()
    return render(request, 'signupAkun.html', {'form': form})