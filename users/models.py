# users/models.py
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractUser, PermissionsMixin):
    class Types(models.TextChoices):
        MENTEE = "MENTEE", "Mentee"
        CASE_MANAGER = "CASE_MANAGER", "Case Manager"

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    gender = models.CharField(
        _("Gender"), max_length=30, choices=GENDER_CHOICES, blank=True, null=True
    )
    type = models.CharField(
        _("User Type"),
        max_length=50,
        choices=Types.choices,
        default=Types.MENTEE,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has verified their email.")
    )
    date_joined = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Type-Based Query Managers
class MenteeManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MENTEE)

class CaseManagerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CASE_MANAGER)

# Profile Models
class MenteeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mentee_profile")
    case_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_mentees",
        limit_choices_to={'type': User.Types.CASE_MANAGER}
    )
    career_interests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} - Mentee Profile"

class CaseManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="case_manager_profile")
    expertise = models.CharField(max_length=200, blank=True)
    max_mentee_capacity = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"{self.user.email} - Case Manager Profile"

# Proxy Models
class Mentee(User):
    objects = MenteeManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.MENTEE
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        try:
            return self.mentee_profile
        except MenteeProfile.DoesNotExist:
            return None

    def assign_case_manager(self, case_manager):
        if self.profile and case_manager.type == User.Types.CASE_MANAGER:
            self.profile.case_manager = case_manager
            self.profile.save()

class CaseManager(User):
    objects = CaseManagerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.CASE_MANAGER
        return super().save(*args, **kwargs)

    @property
    def profile(self):
        try:
            return self.case_manager_profile
        except CaseManagerProfile.DoesNotExist:
            return None

    def get_mentee_count(self):
        return self.assigned_mentees.count()

    def can_accept_more_mentees(self):
        return self.profile and self.get_mentee_count() < self.profile.max_mentee_capacity

# Signal to create profiles
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created or instance.type != User.objects.get(pk=instance.pk).type:
        if instance.type == User.Types.MENTEE:
            MenteeProfile.objects.get_or_create(user=instance)
            CaseManagerProfile.objects.filter(user=instance).delete()
        elif instance.type == User.Types.CASE_MANAGER:
            CaseManagerProfile.objects.get_or_create(user=instance)
            MenteeProfile.objects.filter(user=instance).delete()