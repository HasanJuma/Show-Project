from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shows/', views.show_list, name='show_list'),
    path('shows/<int:show_id>/', views.show_detail, name='show_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile'),          
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password/change/', views.change_password, name='change_password'),
]
