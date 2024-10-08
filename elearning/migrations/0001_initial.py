# Generated by Django 5.0.6 on 2024-08-29 06:17

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('length_in_weeks', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('date_added', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startMonth', models.CharField(choices=[('JAN', 'January'), ('FEB', 'Februray'), ('MAR', 'March'), ('APR', 'April'), ('MAY', 'May'), ('JUN', 'June'), ('JUL', 'July'), ('AUG', 'August'), ('SEP', 'September'), ('OCT', 'October'), ('NOV', 'November'), ('DEC', 'December')], max_length=3)),
                ('startYear', models.PositiveSmallIntegerField(default=2024, validators=[django.core.validators.MinValueValidator(2024), django.core.validators.MaxValueValidator(9999)])),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=256, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('week', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)])),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now=True)),
                ('file', models.FileField(upload_to='elearning/uploads/courseMateral/')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='elearning.courses')),
            ],
            options={
                'verbose_name_plural': 'Course Material',
            },
        ),
        migrations.CreateModel(
            name='CourseFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('feedback', models.TextField()),
                ('date_posted', models.DateField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='elearning.courses')),
            ],
            options={
                'verbose_name_plural': 'Course Feedback',
            },
        ),
        migrations.CreateModel(
            name='CourseDueDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now=True)),
                ('date_due', models.DateField(auto_now=True)),
                ('file', models.FileField(upload_to='elearning/uploads/dueDates/')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='elearning.courses')),
            ],
            options={
                'verbose_name_plural': 'Course Due Dates',
            },
        ),
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pen', 'Pending'), ('App', 'Approved'), ('Dec', 'Declined'), ('Blo', 'Blocked')], max_length=3)),
                ('note', models.CharField(max_length=256)),
                ('registration_date', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='elearning.courses')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Registrations',
            },
        ),
        migrations.AddField(
            model_name='courses',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='elearning.semester'),
        ),
        migrations.CreateModel(
            name='StatusUpdates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=256)),
                ('date_added', models.DateField(auto_now=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Status Updates',
            },
        ),
    ]
