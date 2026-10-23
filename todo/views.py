from datetime import date

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import TodoForm
from .models import Todo


@require_GET
def todo_list(request):
    query = request.GET.get('q', '').strip()
    created_date = request.GET.get('created_date', '').strip()
    todos = Todo.objects.all()

    if query:
        todos = todos.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if created_date:
        try:
            parsed_date = date.fromisoformat(created_date)
        except ValueError:
            todos = todos.none()
        else:
            todos = todos.filter(created_at__date=parsed_date)

    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'query': query,
        'created_date': created_date,
    })


@require_http_methods(['GET', 'POST'])
def todo_create(request):
    form = TodoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task created successfully.')
        return redirect('todo_list')
    return render(request, 'todo/create.html', {
        'form': form,
        'today': timezone.localdate(),
        'submit_label': 'Create Task',
    })


@require_http_methods(['GET', 'POST'])
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    form = TodoForm(request.POST or None, instance=todo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('todo_list')
    return render(request, 'todo/edit.html', {
        'form': form,
        'todo': todo,
        'submit_label': 'Save Changes',
    })


@require_http_methods(['GET', 'POST'])
def todo_confirm_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('todo_list')
    return render(request, 'todo/confirm_delete.html', {'todo': todo})


@require_POST
def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = Todo.Status.COMPLETED
    todo.save(update_fields=['status'])
    messages.success(request, 'Task marked as complete.')
    return redirect('todo_list')


@require_POST
def todo_cancel(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.status = Todo.Status.CANCELLED
    todo.save(update_fields=['status'])
    messages.success(request, 'Task cancelled.')
    return redirect('todo_list')
