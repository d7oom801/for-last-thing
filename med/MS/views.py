from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import UserSerializer, DoctorSerializer, PatientSerializer, FeedbackSerializer, \
    SpecializationSerializer, AvailableSerializer, AppointmentSerializer, ClinicSerializer
from .models import CustomUser, Doctor, Patient, Feedback, Specialization, Available, Appointment, Clinic


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                "detail": "Successfully logged in.",
                "user_id": user.pk,
                "user_type": user.user_type,
                "username": user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class User_view(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class Clinic_view(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class Doctor_view(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'user'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class Patient_view(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticated]


class Feedback_view(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class Specialization_view(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

    # FIX: Allow anyone to see specializations so the Home page doesn't crash for guests!
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


class CheckSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # FIX: Send all the user details so the Profile page can fill the boxes
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "user_type": request.user.user_type,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone_number": request.user.phone_number,
        })


class Available_view(viewsets.ModelViewSet):
    serializer_class = AvailableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'doctor':
            return Available.objects.filter(doctor__user=user)
        elif user.user_type == 'patient':
            return Available.objects.filter(status=True)
        return Available.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'doctor':
            raise PermissionDenied("Only doctors can create available times.")
        doctor_profile = user.doctor_profile
        serializer.save(doctor=doctor_profile)


class Appointment_view(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient':
            return Appointment.objects.filter(patient__user=user)
        elif user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'patient':
            raise PermissionDenied("Only patients can book appointments.")

        patient_profile = user.patient_profile
        doctor = serializer.validated_data.get('doctor')
        date = serializer.validated_data.get('date')
        time = serializer.validated_data.get('time')

        available_slot = Available.objects.filter(doctor=doctor, date=date, time=time, status=True).first()

        if not available_slot:
            raise ValidationError({"detail": "This time slot is not available or has already been booked."})

        available_slot.status = False
        available_slot.save()
        serializer.save(patient=patient_profile, status='pending')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.user_type != 'doctor' or instance.doctor.user != user:
            raise PermissionDenied("Only the assigned doctor can update this appointment.")

        status_update = request.data.get('status')
        if status_update is False or status_update == 'declined':
            instance.status = 'declined'
            available_slot = Available.objects.filter(doctor=instance.doctor, date=instance.date,
                                                      time=instance.time).first()
            if available_slot:
                available_slot.status = True
                available_slot.save()
        elif status_update is True or status_update == 'accepted':
            instance.status = 'accepted'

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)