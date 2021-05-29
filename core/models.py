from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    location = models.CharField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    account_type = models.ChoiceField(choices=[('teacher', 'teacher'), ('student', 'student')])


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
