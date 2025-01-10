from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('view_or_edit_profile/', views.view_or_edit_profile, name='view_or_edit_profile'),
    path('cats/', views.view_cats, name='cats'),
    path('adopt/<int:cat_id>/', views.create_adoption_request, name='adopt'),
    path('adoption_requests/', views.view_adoption_requests, name='adoption_requests'),
    path('cancel_adoption/<int:adoption_request_id>', views.delete_adoption_request, name='cancel_adoption'),
]