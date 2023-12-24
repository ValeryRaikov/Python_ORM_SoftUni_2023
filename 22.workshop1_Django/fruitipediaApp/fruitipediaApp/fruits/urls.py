from django.contrib import admin
from django.urls import path, include

from fruitipediaApp.fruits import views

urlpatterns = [
    path('', views.index, name=''),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fruit', views.create_fruit, name='create-fruit'),
    path('fruit/int:fruit_pk', include([
        path('details', views.details_fruit, name='detail-fruit'),
        path('edit', views.edit_fruit, name='edit-fruit'),
        path('delete', views.delete_fruit, name='delete-fruit'),
    ])),
    path('category', views.create_category, name='create-category'),
]
