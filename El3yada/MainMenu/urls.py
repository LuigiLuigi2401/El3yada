from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'appointments', views.AppointmentViewSet,basename='appointmentsAPI')
router.register(r'patients', views.PatientViewSet,basename='patientsAPI')

urlpatterns=[
    path("api/",include(router.urls)),
    path("",views.index,name='index'),
    path("adduser/",views.AddUsers,name="addusers"),
    path("addappointment/",views.appointmentadd,name="addappointments"),
    path("patient/create/",views.PatientAdd,name="patientadd"),
    path("patient/<int:Ser>",views.PatientView,name="patientview"),
    path('appointment/<int:Aser>',views.AppointmentView,name='updateappointment'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]