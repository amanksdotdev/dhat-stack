# In a file called [project root]/components/calendar/calendar.py
from django_components import Component, register


@register("counter")
class Counter(Component):
    template_name = "counter/counter.html"
