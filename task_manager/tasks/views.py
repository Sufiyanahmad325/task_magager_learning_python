from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import Task
from .forms import TaskForm




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
    query = request.GET.get('q' , "") # ye line batao mujhe 
    status = request.GET.get('status', "")
    sort_by = request.GET.get('sort', 'newest')
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    if query:
          tasks = tasks.filter(title__icontains=query)

    if status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)


    if sort_by == 'newest':
        tasks = tasks.order_by('-created_at')

    elif sort_by == 'oldest':
        tasks = tasks.order_by('created_at')

    elif sort_by == 'high':
        tasks = tasks.order_by('priority')

    return render(request, 'tasks/dashboard.html', 
                  {
                      'tasks': tasks ,
                        'query': query,
                        'status': status,
                        'sort_by': sort_by
                  }
                )





@login_required
def create_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('dashboard')
        
    else:
        form = TaskForm()
    
    return render(request , 'tasks/create_task.html' , {'form':form})



@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task , id=task_id , user = request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    else:
        form = TaskForm(instance=task)
    
    return render(request , 'tasks/edit_task.html' , {'form':form})



@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return redirect('dashboard')




@login_required
def toggle_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    task.is_completed = not task.is_completed
    task.save()

    return redirect('dashboard')





