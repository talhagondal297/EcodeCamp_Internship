from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        task_name = request.POST.get('task')
        if task_name:
            Task.objects.create(name=task_name)
        return redirect('task_list')
    return render(request, 'todo_app/add_task.html')

def remove_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

def delete_all_tasks(request):
    if request.method == 'POST':
        Task.objects.all().delete()
    return redirect('task_list')
