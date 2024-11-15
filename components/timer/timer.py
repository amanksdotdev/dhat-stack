from django_components import Component, register

@register("timer")
class Timer(Component):
    template_name = "timer/timer.html"
    
    class Media:
        js = "timer.js"
        
