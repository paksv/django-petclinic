from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('<int:pk>/', views.VisitDetailView.as_view(), name='visit-detail'),
    path('new/', views.VisitCreateView.as_view(), name='visit-create'),
    path('pet/<int:pet_id>/new/', views.VisitCreateView.as_view(), name='visit-create-for-pet'),
    path('<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit-update'),
]