from django.urls import path
from . import views

app_name = 'owners'

urlpatterns = [
    path('', views.OwnerListView.as_view(), name='owner-list'),
    path('search/', views.search_owners, name='owner-search'),
    path('new/', views.OwnerCreateView.as_view(), name='owner-create'),
    path('<int:pk>/', views.OwnerDetailView.as_view(), name='owner-detail'),
    path('<int:pk>/edit/', views.OwnerUpdateView.as_view(), name='owner-update'),
]