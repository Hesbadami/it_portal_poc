from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users),
    path('users/add_user/', views.add_user),
    path('user/<int:user_id>/', views.manage_user),
    path('delete_user/<int:user_id>/', views.delete_user),
    path('companies/', views.companies),
    path('companies/add_company/', views.add_company),
    path('company/<int:company_id>/', views.manage_company),
    path('delete_company/<int:company_id>/', views.delete_company)
]