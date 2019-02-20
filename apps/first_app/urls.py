from django.conf.urls import url
from . import views  
import json

from django.contrib import admin
from apps.first_app.models import User as U
class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)

urlpatterns = [
    # Renders
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^account/edit$', views.edit_account),
    url(r'^profile$', views.profile),
    url(r'^nutrition$', views.nutrition),
    url(r'^workouts$', views.workouts),
    url(r'^workout/view/(?P<id>\d+)$', views.view_workout),
    # Posts
    url(r'^user/logout$', views.logout_user),
    url(r'^user/login$', views.login_user),
    url(r'^user/register$', views.register_user),
    url(r'^workout/add$', views.add_workout),
    url(r'^food/add$', views.add_food),
    url(r'^account/edit/(?P<id>\d+)$', views.edit_user_account),
    url(r'^workout/edit/(?P<id>\d+)$', views.edit_workout),
    url(r'^food/edit/(?P<id>\d+)$', views.edit_food),
    url(r'^workout/delete/(?P<id>\d+)$', views.delete_workout),
    url(r'^food/delete/(?P<id>\d+)$', views.delete_food),
    url(r'^search/workouts$', views.search_workouts),
]                            

