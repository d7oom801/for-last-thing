from modeltranslation.translator import register, TranslationOptions
from .models import Doctor, Specialization, Clinic, CustomUser

@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    # This translates the actual names of the doctors and patients!
    fields = ('first_name', 'last_name',)

@register(Specialization)
class SpecializationTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('clinic_name', 'qualification', 'about_me',)

@register(Clinic)
class ClinicTranslationOptions(TranslationOptions):
    fields = ('name', 'address',)