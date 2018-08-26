from django import template
register = template.Library()

@register.simple_tag
def get_key_from_list(List, index, key=None):
    if key is None:
        return List[int(index)]
    else:
        return List[int(index)].get(str(key), None)