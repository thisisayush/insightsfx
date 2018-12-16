from django.urls import path, include
from apps.accounts.views import EnableUser, RemoveUser, SuspendUser, ActivateUser

from . import views as v

app_name = "dashboard"

urlpatterns = [
    path("users/browse/", v.BrowseUsersView, name="list-users"),
    path("profile/", v.UserEditView, name="profile"),
    path("settings/", v.ManageSiteView, name="site-management"),
    path("settings/users/manage/edit/<int:userid>/", v.UserEditView, name="edit-user"),
    path("settings/users/manage/suspend/<int:userid>/", SuspendUser, name="suspend-user"),
    path("settings/users/manage/enable/<int:userid>/", EnableUser, name="enable-user"),
    path("settings/users/manage/remove/<int:userid>/", RemoveUser, name="remove-user"),
    path("settings/users/manage/activate/<int:userid>/", ActivateUser, name="activate-user"),
    path("list/data", v.ListData, name="list-data"),
    path("", v.IndexView, name="home"),
]
