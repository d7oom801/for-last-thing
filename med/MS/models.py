from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('clinic', 'Clinic'),
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')

    def __str__(self):
        return self.username


class Clinic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='clinic_profile', null=True,
                                blank=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.IntegerField(null=True, blank=True)
    gender_choices = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    age = models.IntegerField(null=True, blank=True)
    gender_choices = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='doctors', null=True,
                                       blank=True)
    clinic_name = models.CharField(max_length=250, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    Med_id = models.CharField(max_length=20, null=True, blank=True)
    about_me = models.TextField(max_length=250, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)

    # ADD THESE TWO LINES:
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Available(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default=True)


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    # UPDATED: Now uses Pending/Accepted/Declined instead of True/False
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Patient: {self.patient.user.first_name} | Dr. {self.doctor.user.first_name} | {self.date.strftime('%d/%m/%Y')}"


class Feedback(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=250)
    choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    rating = models.IntegerField(choices=choices)

    def __str__(self):
        return f"Feedback from {self.appointment.patient.user.first_name}"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'doctor':
            Doctor.objects.create(user=instance)
        elif instance.user_type == 'patient':
            Patient.objects.create(user=instance)
        # UPDATED: Auto-create a clinic profile when a Clinic user registers
        elif instance.user_type == 'clinic':
            Clinic.objects.create(user=instance, name=f"{instance.username} Clinic")


class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Unknown User"
        return f"{username} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"