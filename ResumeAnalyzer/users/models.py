from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_regular_user = models.BooleanField(default=True, help_text="Indicates if this is a regular user (not admin)")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        # If user is a superuser, mark as not regular user
        is_regular = not (instance.is_superuser or instance.is_staff)
        UserProfile.objects.create(
            user=instance,
            is_regular_user=is_regular
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        # Update is_regular_user based on superuser/staff status
        instance.profile.is_regular_user = not (instance.is_superuser or instance.is_staff)
        instance.profile.save()
    else:
        # Create profile if it doesn't exist
        is_regular = not (instance.is_superuser or instance.is_staff)
        UserProfile.objects.create(
            user=instance,
            is_regular_user=is_regular
        )
