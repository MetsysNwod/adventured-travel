from django.contrib import admin

# Register your models here.
from .models import Lender, Items, Service, ServiceInstance, Language

admin.site.register(Items)
admin.site.register(Language)


class ServicesInline(admin.TabularInline):

    model = Service


@admin.register(Lender)
class LenderAdmin(admin.ModelAdmin):

    list_display = ('last_name',
                    'first_name', 'contract_start', 'contract_ends')
    fields = ['first_name', 'last_name', ('contract_start', 'contract_ends')]
    inlines = [ServicesInline]

class ServicesInstanceInline(admin.TabularInline):

    model = ServiceInstance


class ServiceAdmin(admin.ModelAdmin):

    list_display = ('activity', 'lender', 'display_items', 'services_cover')
    inlines = [ServicesInstanceInline]


admin.site.register(Service, ServiceAdmin)

@admin.register(ServiceInstance)
class ServiceInstanceAdmin(admin.ModelAdmin):

    list_display = ('service', 'status', 'borrower', 'engaged', 'id')
    list_filter = ('status', 'engaged')

    fieldsets = (
        (None, {
            'fields': ('service', 'location', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'engaged', 'borrower')
        }),
    )

# Apartado registro new user

from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'bio', 'web')
    
