from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        first = cleaned_data.get("first_name")
        last = cleaned_data.get("last_name")

        if first == "":
            raise forms.ValidationError("Please add your first name")
        if last == "":
            raise forms.ValidationError("Please add your last name")
        
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(ModelForm):
    class Meta:
        model = AppUser
        fields = ('image',)

class CourseCreateForm(ModelForm):
    class Meta:
        model = Courses
        fields = ['code', 'name', 'description', 'length_in_weeks', 'semester']

class FeedbackCreateForm(ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['student_id', 'course_id', 'rating', 'feedback']
        widgets = {'student_id': forms.HiddenInput(), 'course_id': forms.HiddenInput()}

class StatusCreateForm(ModelForm):
    class Meta:
        model = StatusUpdates
        fields = ['user', 'status']
        widgets = {'user': forms.HiddenInput()}

class Register_Student_to_CourseForm(ModelForm):
    class Meta:
        model = Registrations
        fields = ['status', 'student', 'course']
        widgets = {'status': forms.HiddenInput(), 'student': forms.HiddenInput(), 'course': forms.HiddenInput()}

class AddDueDate(ModelForm):
    class Meta:
        model = CourseDueDates
        fields = ['course_id', 'type', 'title', 'description', 'date_due']
        widgets = {'course_id': forms.HiddenInput()}

class AddMaterial(ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['course_id', 'type', 'title', 'week', 'description', 'file']
        widgets = {'course_id': forms.HiddenInput()}