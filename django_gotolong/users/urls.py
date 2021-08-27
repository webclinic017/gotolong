from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django_gotolong.users import views as users_views
from django_gotolong.users.views import UsersListView

urlpatterns = [
    path('index/', users_views.index, name="home"),
    path('list/', UsersListView.as_view(), name='users-list'),
    path('sign-up/', users_views.sign_up, name="users-sign-up")
]
