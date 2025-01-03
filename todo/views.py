from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Todo


class TodoView(LoginRequiredMixin, View):
    template_name = 'todo.html'

    def get(self, request):
        if request.htmx:
            if request.session.get('error'):
                self.template_name = 'todo.html#error'
                context = {'error': request.session['error']}
                del request.session['error']
                response = render(request, self.template_name, context)
                response['HX-Retarget'] = '#todo'
                response['HX-Reswap'] = 'afterend'
                return response

            if request.session.get('todo_id'):
                self.template_name = 'todo.html#todoitem'
                todoitem = get_object_or_404(
                    Todo, id=request.session['todo_id'])
                del request.session['todo_id']
                context = {'todo': todoitem}
                return render(request, self.template_name, context)

        context = {"todos": Todo.objects.filter(user=request.user).order_by('-created_at')}
        return render(request, self.template_name, context)

    def post(self, request):
        title = request.POST.get('todo')
        if not title:
            request.session['error'] = 'input is required'
            return redirect('todo')
        todoitem = Todo.objects.create(title=title, user=request.user)
        request.session['todo_id'] = todoitem.id
        return redirect('todo')


@login_required()
def mark_done(request, id):
    todoitem = get_object_or_404(Todo, pk=id)
    print(request.POST.get('done'))
    todoitem.completed = True if request.POST.get('done') == 'true' else False
    todoitem.save()
    request.session['todo_id'] = todoitem.id
    return redirect('todo')


@login_required()
def delete_todo(request, id):
    todoitem = get_object_or_404(Todo, pk=id)
    if todoitem.user == request.user:
        todoitem.delete()
    else:
        return HttpResponse(401)
    return HttpResponse(status=200)
