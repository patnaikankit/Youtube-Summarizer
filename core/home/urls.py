from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('genarate-summary', views.genarate_summary, name='genarate-summary'),
    path('list', views.list, name='list'),
    path('list-details/<int:pk>/', views.list_details, name='list-details'),
]