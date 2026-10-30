from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Task



def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

    else:
        form = SignUpForm()

    return render(request, 'tasks/signup.html', {'form': form})



#  Login

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        form = AuthenticationForm(request , data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request , user)
            return redirect("dashboard")
        
    else:
        form = AuthenticationForm(request)

    return render(request, 'tasks/login.html', {'form': form})





def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')



@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})