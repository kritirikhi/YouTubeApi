from django.urls import path,include 
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('filteraction',views.filteraction,name='filter'),
    path('api/v1/search',views.search,name='searchapi'),
    path('api/v1/view',views.viewvideo,name='viewapi'),
    path('searchview',views.searchview,name='searchview'),
    path('searchmain',views.searchmain,name='searchmain'),
]