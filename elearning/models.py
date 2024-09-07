from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator 

class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='elearning/uploads/profilePhotos/%Y/%m/%d', blank=True, null=True)

    def __unicode__(self):
        return self.user.username
    
    def __str__(self):
        return f"{self.user.username} {self.user.first_name} {self.user.last_name}"


class Semester(models.Model):
    class Months(models.TextChoices):
        JANUARY = "JAN"
        FEBRUARY = "FEB"
        MARCH = "MAR"
        APRIL = "APR"
        MAY = "MAY"
        JUNE = "JUN"
        JULY = "JUL"
        AUGUST = "AUG"
        SEPTEMBER = "SEP"
        OCTOBER = "OCT"
        NOVEMBER = "NOV"
        DECEMBER = "DEC"

    startMonth = models.CharField(max_length=3, choices=Months)
    startYear = models.PositiveSmallIntegerField(null=False, default=datetime.datetime.now().year, validators=[MinValueValidator(datetime.datetime.now().year), MaxValueValidator(9999)])

    def __str__(self):
        return f"{self.startMonth} {self.startYear}"

class StatusUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length = 256)
    date_added = models.DateField(auto_now = True)

    class Meta:
        verbose_name_plural = "Status Updates"

class Courses(models.Model):
    code = models.CharField(max_length = 10, null=False)
    name = models.CharField(max_length = 256, null=False)
    description = models.TextField(null=False)
    length_in_weeks = models.PositiveIntegerField(default = 1, null=False, validators=[MinValueValidator(1), MaxValueValidator(52)])
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    date_added = models.DateField(auto_now = True)

    class Meta:
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return f"{self.code} - {self.name} - {self.semester}"

class CourseMaterial(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length = 256, null=False)
    title = models.CharField(max_length = 256, null=False)
    week = models.PositiveIntegerField(default = 1, null=False, validators=[MinValueValidator(1), MaxValueValidator(52)])
    description = models.TextField(null=False)
    date_added = models.DateField(auto_now = True, null=False)
    file = models.FileField(upload_to='elearning/uploads/courseMateral/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name_plural = "Course Material"

class CourseDueDates(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length = 256, null=False)
    title = models.CharField(max_length = 256, null=False)
    description = models.TextField(null=False)
    date_added = models.DateField(auto_now = True, null=False)
    date_due = models.DateField(null=False)

    class Meta:
        verbose_name_plural = "Course Due Dates"

class Registrations(models.Model):
    class Status(models.TextChoices):
        Pending = "PENDING"
        Approved = "APPROVED"
        Declined = "DECLINED"
        Blocked = "BLOCKED"

    status = models.CharField(max_length=8, choices=Status)
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Courses, null = False, on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=256, blank=True)
    registration_date = models.DateField(auto_now = True, null=False)

    class Meta:
        verbose_name_plural = "Registrations"
        unique_together = ('student', 'course')
    
class CourseFeedback(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    rating = models.PositiveIntegerField(default = 1, null=False, validators=[MinValueValidator(0), MaxValueValidator(5)])
    feedback = models.TextField()
    date_posted = models.DateField(auto_now = True, null=False)

    class Meta:
        verbose_name_plural = "Course Feedback"
    
class ChatMessages(models.Model):
    text = models.CharField(max_length=256)
    room = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chat Messages"