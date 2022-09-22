from importlib.resources import path
from django.urls import path
#from django.urls import re_path as url
from . import views


urlpatterns = [
    path(r'', views.index, name='index'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='service_detail'),
    path('lenders/', views.LenderListView.as_view(), name='lenders'),
    path('lender/<int:pk>',
         views.LenderDetailView.as_view(), name='lender-detail'),
]

urlpatterns += [
    path('myservices/', views.AvailableServicesByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.AvailableServicesAllListView.as_view(), name='all-borrowed'),
]

# Add URLConf for manager to renew a service.
urlpatterns += [
    path('service/<uuid:pk>/renew/', views.renew_service_manager, name='renew-services-manager'),
#    url(r'^service/(?P<pk>[-\w]+)/renew/$', views.renew_service_manager, name='renew_service_manager'),
]

# Add URLConf to create, update, and delete lenders
urlpatterns += [
    path('lender/create/', views.LenderCreate.as_view(), name='lender-create'),
    path('lender/<int:pk>/update/', views.LenderUpdate.as_view(), name='lender-update'),
    path('lender/<int:pk>/delete/', views.LenderDelete.as_view(), name='lender-delete'),
]

# Add URLConf to create, update, and delete services
urlpatterns += [
    path('service/create/', views.ServiceCreate.as_view(), name='service-create'),
    path('service/<int:pk>/update/', views.ServiceUpdate.as_view(), name='service-update'),
    path('service/<int:pk>/delete/', views.ServiceDelete.as_view(), name='service-delete'),
]

# registro new user

from adventuretravel.views import SignUpView

urlpatterns += [
    path('accounts/', SignUpView.as_view(),name='sign_up'),
]