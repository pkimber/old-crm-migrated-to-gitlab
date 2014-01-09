from django import template


register = template.Library()


@register.inclusion_tag('crm/_menu.html')
def crm_menu():
    return {}
