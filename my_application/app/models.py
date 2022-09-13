import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


class Report(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=250, unique=False, default="")
    Creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator', on_delete=models.CASCADE, null=True)
    data = models.FileField(upload_to="files/", validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    output_data = models.FileField(upload_to="files/output")
    timestamp = models.DateTimeField(auto_now_add=True)
    total_local_transactions = models.FloatField(default=0.0)
    total_initial_transactions = models.FloatField(default=0.0)
    no_of_initial_transactions = models.IntegerField(default=0)
    no_of_initial_countries = models.IntegerField(default=0)
    no_of_local_countries = models.IntegerField(default=0)
    no_of_cycles_flows = models.IntegerField(default=0)
    no_complete_local_transactions = models.IntegerField(default=0)
    no_of_local_transactions = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_person(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_person, sender=User)
