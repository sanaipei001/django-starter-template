# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, MenteeProfile, CaseManagerProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print(f"Signal triggered for {instance.email}, created={created}, type={instance.type}")
    if created or (not created and instance.type != User.objects.get(pk=instance.pk).type):
        if instance.type == User.Types.MENTEE:
            MenteeProfile.objects.get_or_create(user=instance)
            CaseManagerProfile.objects.filter(user=instance).delete()
        elif instance.type == User.Types.CASE_MANAGER:
            CaseManagerProfile.objects.get_or_create(user=instance)
            MenteeProfile.objects.filter(user=instance).delete()
    print(f"Post-signal: Mentee profiles={MenteeProfile.objects.filter(user=instance).count()}, CaseManager profiles={CaseManagerProfile.objects.filter(user=instance).count()}")