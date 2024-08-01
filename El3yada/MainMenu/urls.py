from django.urls import path,include,register_converter
from rest_framework import routers
from . import views
from datetime import datetime,date
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'appointments', views.AppointmentViewSet,basename='appointmentsAPI')
router.register(r'patients', views.PatientViewSet,basename='patientsAPI')
router.register(r'services', views.ServiceViewSet,basename='servicesAPI')
router.register(r'payments', views.PaymentsViewSet,basename='paymentsAPI')
router.register(r'today',views.AppointmentDayViewSet,basename='dayviewAPI')

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/addnewapp/', views.AddNewAppointmentView.as_view(), name='addnewapp'),
    path('api/getapppay/', views.GetAppointmentToPayForView.as_view(), name='getapppay'),
    path("api/addnewpat/",views.AddNewPatientView.as_view(),name="addnewpat"),
    path('api/editapp/<int:Aser>', views.EditAppointmentView.as_view(), name='editapp'),
    path('api/paydiag/<int:Aser>', views.PayDiagnosisAppointmentView.as_view(), name='paydiag'),
    path('api/payserv/<int:Aser>', views.PayServiceAppointmentView.as_view(), name='payserv'),
    path('api/editpat/<int:Ser>', views.EditPatientView.as_view(), name='editpat'),
    path('api/add_debts/<int:Ser>/<int:Aser>', views.AddDebtsView.as_view(), name='add_debts'),
    path('api/doctors/', views.DoctorView.as_view(), name='doctors'),
    path("",views.index,name='index'),
    path("adduser/",views.AddUsers,name="addusers"),
    path("addappointment/<int:Ser>",views.appointmentadd,name="addappointments"),
    path("patient/create/",views.PatientAdd,name="patientadd"),
    path("patient/<int:Ser>",views.PatientView,name="patientview"),
    path('appointment/<int:Aser>',views.AppointmentView,name='updateappointment'),
    path('payment/<int:Pser>',views.payment,name='payment'),
    path('appointment/<date:Adate>',views.viewday,name='viewdayappointment'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/count/<str:category>/<int:rowsper>', views.count,name='countview')
]