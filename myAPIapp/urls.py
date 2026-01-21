from django.urls import path
from . import views

urlpatterns = [
    # Vista principal
    path('', views.index, name='index'),
    
    # Inicializar base de datos desde API
    path('initialize/', views.initialize_database, name='initialize_database'),
    
    # CRUD de personajes
    path('character/<int:pk>/', views.character_detail, name='character_detail'),
    path('character/create/', views.character_create, name='character_create'),
    path('character/<int:pk>/edit/', views.character_edit, name='character_edit'),
    path('character/<int:pk>/delete/', views.character_delete, name='character_delete'),
]