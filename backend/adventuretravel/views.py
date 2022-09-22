from urllib import request
from django.shortcuts import render

# Create your views here.

from .models import Service, Lender, ServiceInstance, Items

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_services = Service.objects.all().count()
    num_instances = ServiceInstance.objects.all().count()
    # Available services
    num_instances_available = ServiceInstance.objects.filter(status__exact='a').count()
    num_lenders = Lender.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_services': num_services, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_lenders': num_lenders,
                 'num_visits': num_visits},
    )


from django.views import generic


class ServiceListView(generic.ListView):
    """Generic class-based view for a list of services."""
    model = Service
    paginate_by = 10
    
class ServiceDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Service

class LenderListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Lender
    paginate_by = 10
    
class LenderDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Lender
    
from django.contrib.auth.mixins import LoginRequiredMixin
    
class AvailableServicesByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing services available to current user."""
    model = ServiceInstance
    template_name = 'adventuretravel/serviceinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ServiceInstance.objects.filter(borrower=self.request.user).filter(status__exact='i').order_by('engaged')
    

from django.contrib.auth.mixins import PermissionRequiredMixin


class AvailableServicesAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all services available. Only visible to users with can_mark_returned permission."""
    model = ServiceInstance
    permission_required = 'adventuretravel.can_mark_returned'
    template_name = 'adventuretravel/serviceinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return ServiceInstance.objects.filter(status__exact='i').order_by('engaged')
    
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

# from .forms import RenewBookForm
from adventuretravel.forms import RenewServiceForm

@login_required
@permission_required('adventuretravel.can_mark_returned', raise_exception=True)
def renew_service_manager(request, pk):
    """View function for renewing a specific ServiceInstance by manager."""
    service_instance = get_object_or_404(ServiceInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewServiceForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            service_instance.engaged = form.cleaned_data['renewal_date']
            service_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewServiceForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'service_instance': service_instance,
    }

    return render(request, 'adventuretravel/service_renew_manager.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Lender

class LenderCreate(PermissionRequiredMixin, CreateView):
    model = Lender
    fields = ['first_name', 'last_name', 'contract_start', 'contract_ends']
    initial = {'contract_ends': '09/06/2022'}
    permission_required = 'adventuretravel.can_mark_returned'
    
class LenderUpdate(PermissionRequiredMixin, UpdateView):
    model = Lender
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'adventuretravel.can_mark_returned'
    
class LenderDelete(PermissionRequiredMixin, DeleteView):
    model = Lender
    success_url = reverse_lazy('lenders')
    permission_required = 'adventuretravel.can_mark_returned'
    
# Classes created for the forms challenge
class ServiceCreate(PermissionRequiredMixin, CreateView):
    model = Service
    fields = ['activity', 'lender', 'description', 'price', 'items', 'language', 'services_cover']
    permission_required = 'adventuretravel.can_mark_returned'

class ServiceUpdate(PermissionRequiredMixin, UpdateView):
    model = Service
    fields = ['activity', 'lender', 'description', 'price', 'items', 'language', 'services_cover']
    permission_required = 'adventuretravel.can_mark_returned'
    
class ServiceDelete(PermissionRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('services')
    permission_required = 'adventuretravel.can_mark_returned'
    
    
# apartado create new user

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.views.generic import CreateView, TemplateView

from .models import Perfil

from .forms import SignUpForm


class SignUpView(CreateView):
    model = Perfil
    form_class = SignUpForm

    def form_valid(self, form):
        '''
        En este parte, si el formulario es valido guardamos lo que se obtiene de él y usamos authenticate para que el usuario incie sesión luego de haberse registrado y lo redirigimos al index
        '''
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('/')

from django.contrib.auth.views import LoginView
class SignInView(LoginView):
    template_name = 'accounts/login.html'