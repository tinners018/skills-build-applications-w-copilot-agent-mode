"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from . import views


# Custom DefaultRouter to override API root view with codespace URL
class CodespaceDefaultRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        original_view = super().get_api_root_view(api_urls)
        def custom_view(request, *args, **kwargs):
            response = original_view(request, *args, **kwargs)
            # Get codespace name from environment
            codespace_name = os.environ.get('CODESPACE_NAME')
            if codespace_name:
                base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
            else:
                # fallback to request host
                base_url = request.build_absolute_uri('/api/')
            # Patch the returned URLs to use the codespace URL
            if isinstance(response.data, dict):
                for k, v in response.data.items():
                    if isinstance(v, str) and v.startswith('/api/'):
                        response.data[k] = base_url + v[len('/api/'):]
            return response
        return custom_view

router = CodespaceDefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.api_root, name='api-root'),
]
