from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    path('new/', views.PetCreateView.as_view(), name='pet-create'),
    path('owner/<int:owner_id>/new/', views.PetCreateView.as_view(), name='pet-create-for-owner'),
    path('<int:pk>/edit/', views.PetUpdateView.as_view(), name='pet-update'),
]