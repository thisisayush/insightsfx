from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import render
from rolepermissions.checkers import has_permission, has_role
from django.conf import settings
from rolepermissions.roles import assign_role, clear_roles, get_user_roles

from apps.accounts import roles as r
from apps.accounts.models import User
from apps.accounts.roles import Admin, Subscriber
from apps.core.constants import database_keys as dk
from apps.core.constants import permissions as p
from apps.core.utils import getOption, getOptions, setOption

from .forms import OptionsForm, PasswordChangeForm, RolesForm, UserForm
from .utils import getTableDataForUsers


@login_required
def IndexView(request):
    if has_role(request.user, Admin):
        context = {
            "count": {
                "users": User.objects.all().count(),
            }
        }
        return render(request, "dashboard/index.html", {"data": context, "map_api_key": settings.MAPMYINDIA_API_KEY})
    elif has_role(request.user, Subscriber):
        context = {
            "map_api_key": settings.MAPMYINDIA_API_KEY
        }
        return render(request, "dashboard/index-subscriber.html", context)
    else:
        raise PermissionDenied("You are not allowed to access this page!")

@login_required
def BrowseUsersView(request):
    if has_permission(request.user, p.READ_USERS):
        enabled_columns = None
        sort_by = None
        sort_order = None
        search = None
        if request.GET.get('enabled_columns', False):
            enabled_columns = request.GET.getlist('enabled_columns')
        if request.GET.get('sort_by', False):
            sort_by = request.GET.get('sort_by')
        if request.GET.get('sort_order', False):
            sort_order = request.GET.get('sort_order')
        if request.GET.get('search', False):
            search = request.GET.get('search')

        tableData = getTableDataForUsers(enabled_columns=enabled_columns,
                                         search=search,
                                         sort_by=sort_by,
                                         sort_order=sort_order
                                         )
        return render(request, "dashboard/list.html", {"tableData": tableData})
    else:
        raise PermissionDenied("You are not allowed to List Users.")


@login_required
def UserEditView(request, userid=None):

    form = None
    user = None
    passForm = None
    rolesForm = None

    if userid == None:
        user = request.user
    elif has_permission(request.user, p.EDIT_USERS) or request.user.id == userid:
        try:
            user = User.objects.get(id=userid)
        except ObjectDoesNotExist as e:
            raise Http404("User Does Not Exist")
    else:
        raise PermissionDenied(
            "You do not have permission to edit/view this user")

    if has_permission(request.user, p.EDIT_USERS):
        roles = []
        for x in get_user_roles(user):
            roles.append(x.display_name)
        rolesForm = RolesForm({'roles': roles})

    form = UserForm(user=request.user, instance=user)
    passForm = PasswordChangeForm(user)

    if request.method == "POST":
        if 'user-submit' in request.POST:
            form = UserForm(user=request.user, data=request.POST or None,
                            files=request.FILES or None, instance=user)
            if form.is_valid():
                form.save()

        if 'password-change' in request.POST:
            passForm = PasswordChangeForm(user, request.POST or None)
            if passForm.is_valid():
                passForm.save()
                update_session_auth_hash(request, user)

        if 'change-role' in request.POST:
            rolesForm = RolesForm(request.POST or None)
            if rolesForm.is_valid():
                User().change_user_role(user, rolesForm.cleaned_data['roles'])

    return render(request, "dashboard/edit-user.html", {'form': form, 'user_context': user, 'passform': passForm, 'rolesForm': rolesForm})


@login_required
def ManageSiteView(request):
    if has_role(request.user, Admin):
        form = None
        if request.method == "POST":
            form = OptionsForm(data = request.POST, files = request.FILES or None)
            if form.is_valid():
                for data in form.cleaned_data:
                    setOption(data, form.cleaned_data[data])
        else:
            form = OptionsForm(initial=getOptions())
        return render(request, "dashboard/settings.html", {"form": form})
    else:
        raise PermissionDenied(
            "You do not have permissions to access this page!")