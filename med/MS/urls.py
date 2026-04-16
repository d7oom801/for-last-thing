from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', User_view, basename='user')
router.register(r'clinics', Clinic_view, basename='clinic') # Added this!
router.register(r'doctors', Doctor_view, basename='doctor')
router.register(r'patients', Patient_view, basename='patient')
router.register(r'feedbacks', Feedback_view, basename='feedback')
router.register(r'specializations', Specialization_view, basename='specialization')
router.register(r'available', Available_view, basename='available')
router.register(r'appointments', Appointment_view, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', GetCSRFToken.as_view(), name='api_csrf'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('me/', CheckSessionView.as_view(), name='check_session'),
]