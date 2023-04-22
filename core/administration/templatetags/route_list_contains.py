
from django import template

register = template.Library()


@register.filter(name="route_list_contains")
def route_list_contains(routeList, route):
    print(route)
    return [r for r in routeList if route in r["route"]]