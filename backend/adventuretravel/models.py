from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class MyModelName(models.Model):
    my_field_name = models.CharField(
    max_length=20, help_text="Enter field documentation")
    class Meta:
        ordering = ["-my_field_name"]
        
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def _str_(self):
        return self.field_name

class Items(models.Model):
    name = models.CharField(
        max_length=200, help_text="Ingrese los elementos que incleye su servicio")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Ingrese idiomas que maneja (por ejemplo, inglés, francés, japonés, etc.)")
    
    def __str__(self):
        return self.name


class Service(models.Model):
    activity = models.CharField(max_length=200)
    lender = models.ForeignKey('Lender', on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        max_length=1000, help_text="Ingrese una breve descripcion de la actividad.")
    price = models.CharField(
        'Price', max_length=13, help_text="Ingrese un precio por la prestacion del servicio.")
    items = models.ManyToManyField(
        Items, help_text="Seleccione el contenido de su actividad.")
    language = models.ManyToManyField(Language, help_text="Seleccione los idiomas que maneja en las actividades.")
    
    class Meta:
        ordering = ['activity', 'lender']
        
        
    def get_absolute_url(self):
        return reverse("service_detail", args=[str(self.id)])

    def display_items(self):
        return ', '.join([items.name for items in self.items.all()[:3] ])
    display_items.short_description = 'Items'
    
    def display_items(self):
        return ', '.join([language.name for language in self.language.all()[:3] ])
    display_items.short_description = 'Language'

    
    def __str__(self):
        return self.activity


class ServiceInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID unico para este servicio")
    service = models.ForeignKey(
        'Service', on_delete=models.SET_NULL, null=True)
    location = models.CharField(
        max_length=200, help_text="Ingrese direccion o coordenadas de la ubicacion en donde se prestara el servicio.")
    engaged = models.DateField(
        null=True, blank=True, help_text="Seleccione una fecha en que estara disponible la actividad.")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.engaged and date.today() > self.engaged)

    AVAILABILITY_STATUS = (
        ('m', 'Maintenance'),
        ('i', 'In progress'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=AVAILABILITY_STATUS,
                              blank=True, default='m', help_text="Disponibilidad del servicio")

    class Meta:
        ordering = ["engaged"]
        permissions = (("can_mark_returned", "Set service as active"),)

    def __str__(self):
        return '%s (%s)' % (self.id, self.service.activity)

class Lender(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contract_start = models.DateField(null=True, blank=True)
    contract_ends = models.DateField('finished', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):

        return reverse('lender-detail', args=[str(self.id)])

    def __str__(self):

        return '{0}, {1}'.format(self.last_name, self.first_name)
    
#Apartado registro Nuevo usuario 

from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    web = models.URLField(blank=True)

    
    def __str__(self): 
        return self.usuario.username

@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()
