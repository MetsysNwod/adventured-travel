# Generated by Django 4.1.1 on 2022-09-15 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(help_text='Ingrese los elementos que incleye su servicio', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ingrese idiomas que maneja (por ejemplo, inglés, francés, japonés, etc.)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Lender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('contract_start', models.DateField(blank=True, null=True)),
                ('contract_ends', models.DateField(blank=True, null=True, verbose_name='finished')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='MyModelName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_field_name', models.CharField(help_text='Enter field documentation', max_length=20)),
            ],
            options={
                'ordering': ['-my_field_name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Ingrese una breve descripcion de la actividad.', max_length=1000)),
                ('price', models.CharField(help_text='Ingrese un precio por la prestacion del servicio.', max_length=13, verbose_name='Price')),
                ('items', models.ManyToManyField(help_text='Seleccione el contenido de su actividad.', to='adventuretravel.items')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adventuretravel.language')),
                ('lender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adventuretravel.lender')),
            ],
            options={
                'ordering': ['activity', 'lender'],
            },
        ),
        migrations.CreateModel(
            name='ServiceInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID unico para este servicio', primary_key=True, serialize=False)),
                ('location', models.CharField(help_text='Ingrese direccion o coordenadas de la ubicacion en donde se prestara el servicio.', max_length=200)),
                ('engaged', models.DateField(blank=True, help_text='Seleccione una fecha en que estara disponible la actividad.', null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Maintenance'), ('i', 'In progress'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Disponibilidad del servicio', max_length=1)),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='adventuretravel.service')),
            ],
            options={
                'ordering': ['engaged'],
                'permissions': (('can_mark_returned', 'Set service as active'),),
            },
        ),
    ]