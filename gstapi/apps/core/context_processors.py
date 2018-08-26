from rolepermissions.roles import get_user_roles
from .constants import permissions as p
from django.conf import settings
from .utils import getOptions

def site_meta_processor(request):
    user_roles = False

    if request.user.is_authenticated:
        user_roles = [role.title for role in get_user_roles(request.user)]

    data = {
        'meta': {
            "debug": settings.DEBUG
        },
        'user_roles': user_roles,
        'constants': {
            'permissions': p
        }
    }
    options = getOptions()
    for key in options:
        data['meta'][key] = options[key]

    return data
