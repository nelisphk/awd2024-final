# Generated by Django 5.1 on 2024-09-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0005_alter_registrations_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseduedates',
            name='date_due',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='courseduedates',
            name='file',
            field=models.FileField(blank=True, upload_to='elearning/uploads/dueDates/'),
        ),
        migrations.AlterField(
            model_name='coursematerial',
            name='file',
            field=models.FileField(blank=True, upload_to='elearning/uploads/courseMateral/'),
        ),
    ]
