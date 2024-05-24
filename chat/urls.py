from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats_panel, name='chats_panel'),
    path('add/', views.add),
    path('detail/<str:chat_id>/', views.detail, name='chat_detail'),
    path('delete/<str:chat_id>/', views.delete),
    path('edit/<str:chat_id>/', views.edit),
    path('view/<str:chat_id>/', views.chat),
    path('view/<str:chat_id>/delete/<str:message_id>/', views.chat),
    path('view/<str:chat_id>/edit/<str:message_id>/', views.chat),
    path('view/<str:chat_id>/insert_above/<str:message_id>/', views.chat),
    path('view/<str:chat_id>/insert_below/<str:message_id>/', views.chat),
]