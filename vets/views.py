from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import Vet, Specialty
from .forms import VetForm

class VetListView(ListView):
    """View for listing all vets"""
    model = Vet
    template_name = 'vets/vet_list.html'
    context_object_name = 'vets'
    paginate_by = 10

    def get_queryset(self):
        """Return all vets ordered by last name, first name"""
        return Vet.objects.all().order_by('last_name', 'first_name')

class VetDetailView(DetailView):
    """View for displaying vet details"""
    model = Vet
    template_name = 'vets/vet_detail.html'
    context_object_name = 'vet'

class VetCreateView(CreateView):
    """View for creating a new vet"""
    model = Vet
    form_class = VetForm
    template_name = 'vets/vet_form.html'
    success_url = reverse_lazy('vets:vet-list')

    def form_valid(self, form):
        messages.success(self.request, 'Veterinarian added successfully.')
        return super().form_valid(form)

class VetUpdateView(UpdateView):
    """View for updating an existing vet"""
    model = Vet
    form_class = VetForm
    template_name = 'vets/vet_form.html'

    def get_success_url(self):
        """Return to the vet's detail page after successful update"""
        return reverse('vets:vet-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Veterinarian updated successfully.')
        return super().form_valid(form)
