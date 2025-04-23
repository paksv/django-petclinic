from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import Visit
from .forms import VisitForm
from pets.models import Pet

class VisitDetailView(DetailView):
    """View for displaying visit details"""
    model = Visit
    template_name = 'visits/visit_detail.html'
    context_object_name = 'visit'

class VisitCreateView(CreateView):
    """View for creating a new visit"""
    model = Visit
    form_class = VisitForm
    template_name = 'visits/visit_form.html'

    def get_form_kwargs(self):
        """Pass pet_id to the form if provided in URL"""
        kwargs = super().get_form_kwargs()
        if 'pet_id' in self.kwargs:
            kwargs['pet_id'] = self.kwargs['pet_id']
        return kwargs

    def get_context_data(self, **kwargs):
        """Add pet to context if pet_id is provided"""
        context = super().get_context_data(**kwargs)
        if 'pet_id' in self.kwargs:
            context['pet'] = get_object_or_404(Pet, pk=self.kwargs['pet_id'])
        return context

    def get_success_url(self):
        """Redirect to pet detail page if visit was created from there"""
        if self.object.pet:
            messages.success(self.request, 'Visit scheduled successfully.')
            return reverse('pets:pet-detail', kwargs={'pk': self.object.pet.pk})
        return reverse('visits:visit-detail', kwargs={'pk': self.object.pk})

class VisitUpdateView(UpdateView):
    """View for updating an existing visit"""
    model = Visit
    form_class = VisitForm
    template_name = 'visits/visit_form.html'

    def get_success_url(self):
        """Return to the pet's detail page after successful update"""
        messages.success(self.request, 'Visit updated successfully.')
        return reverse('pets:pet-detail', kwargs={'pk': self.object.pet.pk})
