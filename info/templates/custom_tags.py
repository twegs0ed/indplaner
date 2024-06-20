from django import template
register = template.Library()


@register.filter(name="div")
def div(value, firm_count):
    return round(value*firm_count/100 , 2)