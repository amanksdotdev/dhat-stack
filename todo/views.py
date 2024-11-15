from django.shortcuts import render, redirect
from django.views import View
from .models import Todo

class TodoView(View):
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
                todoitem = Todo.objects.get(id=request.session['todo_id'])
                del request.session['todo_id']
                context = {'todo': todoitem}
                return render(request, self.template_name, context)
            
        context = {"todos": Todo.objects.all()}               
        return render(request, self.template_name, context)
    
    def post(self, request):
        title = request.POST.get('todo')
        if not title:
            request.session['error'] = 'input is required'
            return redirect('todo')
        todoitem = Todo.objects.create(title=title)
        request.session['todo_id'] = todoitem.id
        return redirect('todo')
    

def delete_todo(request, id):
    pass
    
