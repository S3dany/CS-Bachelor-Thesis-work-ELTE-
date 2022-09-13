# Generated by Django 3.2 on 2021-05-28 20:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=250)),
                ('data', models.FileField(upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('output_data', models.FileField(upload_to='files/output')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('total_local_transactions', models.FloatField(default=0.0)),
                ('total_initial_transactions', models.FloatField(default=0.0)),
                ('no_of_initial_transactions', models.IntegerField(default=0)),
                ('no_of_initial_countries', models.IntegerField(default=0)),
                ('no_of_local_countries', models.IntegerField(default=0)),
                ('no_of_cycles_flows', models.IntegerField(default=0)),
                ('no_complete_local_transactions', models.IntegerField(default=0)),
                ('no_of_local_transactions', models.IntegerField(default=0)),
                ('Creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
