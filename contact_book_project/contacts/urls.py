from django.urls import path
from contacts import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='contact_create'),
    path('replace/', views.contact_replace, name='contact_replace'),
    path('update/<int:pk>/', views.contact_update, name='contact_update'),
    path('delete/<int:pk>/', views.contact_delete, name='contact_delete'),
    path('confirm_update/<int:pk>/', views.confirm_update, name='confirm_update'),
]
