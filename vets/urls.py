from django.urls import path
from . import views

app_name = 'vets'

urlpatterns = [
    path('', views.VetListView.as_view(), name='vet-list'),
    path('<int:pk>/', views.VetDetailView.as_view(), name='vet-detail'),
    path('new/', views.VetCreateView.as_view(), name='vet-create'),
    path('<int:pk>/edit/', views.VetUpdateView.as_view(), name='vet-update'),
]