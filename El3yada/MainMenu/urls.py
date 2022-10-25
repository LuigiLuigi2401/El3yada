from django.urls import path,include,register_converter
from rest_framework import routers
from . import views
from datetime import datetime,date

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'appointments', views.AppointmentViewSet,basename='appointmentsAPI')
router.register(r'patients', views.PatientViewSet,basename='patientsAPI')

class DateConverter:
      regex = r"\d{4}-\d{1,2}-\d{1,2}"
      format = "%Y-%m-%d"

      def to_python(self, value: str) -> date:
          return datetime.strptime(value, self.format).date()

      def to_url(self, value: date) -> str:
          return value.strftime(self.format)

register_converter(DateConverter, "date")

print(date)

urlpatterns=[
    path("api/",include(router.urls)),
    path("",views.index,name='index'),
    path("adduser/",views.AddUsers,name="addusers"),
    path("addappointment/",views.appointmentadd,name="addappointments"),
    path("patient/create/",views.PatientAdd,name="patientadd"),
    path("patient/<int:Ser>",views.PatientView,name="patientview"),
    path('appointment/<int:Aser>',views.AppointmentView,name='updateappointment'),
    path('appointment/<date:Adate>',views.viewday,name='viewdayappointment'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]