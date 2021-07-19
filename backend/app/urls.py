"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import HomeView
from garpix_auth.views import LogoutView, LoginView
from garpix_auth.rest.obtain_auth_token import obtain_auth_token

urlpatterns = [
    path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    # garpix_auth
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="authorize"),
    path('api/login/', obtain_auth_token),
]
