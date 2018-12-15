"""fms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('accounts/', include('apps.accounts.urls', namespace="accounts")),
    path('dashboard/', include('apps.dashboard.urls', namespace="dashboard")),
    path("", RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL), name="home" ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'
handler403 = 'apps.core.views.permission_denied'
handler400 = 'apps.core.views.bad_request'