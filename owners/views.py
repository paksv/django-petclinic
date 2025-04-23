from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Owner
from .forms import OwnerForm

class OwnerListView(ListView):
    """View for listing all owners"""
    model = Owner
    template_name = 'owners/owner_list.html'
    context_object_name = 'owners'
    paginate_by = 10

    def get_queryset(self):
        """
        Override get_queryset to implement search functionality
        """
        queryset = Owner.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query)
            )
        return queryset

class OwnerDetailView(DetailView):
    """View for displaying owner details"""
    model = Owner
    template_name = 'owners/owner_detail.html'
    context_object_name = 'owner'

class OwnerCreateView(CreateView):
    """View for creating a new owner"""
    model = Owner
    form_class = OwnerForm
    template_name = 'owners/owner_form.html'
    success_url = reverse_lazy('owners:owner-list')

class OwnerUpdateView(UpdateView):
    """View for updating an existing owner"""
    model = Owner
    form_class = OwnerForm
    template_name = 'owners/owner_form.html'

    def get_success_url(self):
        """Return to the owner's detail page after successful update"""
        return reverse_lazy('owners:owner-detail', kwargs={'pk': self.object.pk})

def search_owners(request):
    """View for searching owners"""
    query = request.GET.get('q', '')
    if query:
        owners = Owner.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query)
        )
    else:
        owners = Owner.objects.all()

    return render(request, 'owners/owner_search.html', {
        'owners': owners,
        'query': query
    })
