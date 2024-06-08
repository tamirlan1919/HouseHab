from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ProfessionalProfile

@receiver(post_save, sender=CustomUser)
def create_professional_profile(sender, instance, created, **kwargs):
    if created and instance.account_type == 'professional':
        ProfessionalProfile.objects.create(user=instance)
