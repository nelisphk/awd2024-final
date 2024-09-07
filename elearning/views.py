from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
from .forms import *

# LOGIC AND DATA FUNCTIONS FOR PAGES TO RUN 
# CHECK  IF STUDENT OR TEACHER
def is_member(user):
    if user.groups.filter(name='Teacher').exists():
        return "Teacher"

    if user.groups.filter(name='Student').exists():
        return "Student"
    
#CREATE A DECORATOR FOR PAGES ONLY TEACHERS MAY ACCESS
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

# RETURN THE BASIC TEMPLATE INFORMATION THAT A PAGE NEEDS TO RENDER
def template_details(request, course_code):
    context={}
    context['role'] = (is_member(request.user))
    context['courses'] = Courses.objects.all()
    context['teachers'] = User.objects.filter(groups__name='Teacher')
    context['students'] = User.objects.filter(groups__name='Student')
    context['user_image'] = AppUser.objects.get(user = request.user).image

    if (context['role'] == "Student"):
        context['courses_enrolled'] = Registrations.objects.filter(status = "APPROVED", student = request.user)

    if (course_code):
        context['selected_course'] = Courses.objects.filter(pk=course_code)[0]

    return context


# REDIRECT VIEWS
# RENDER THE INDEX
def index(request):
        #Import the base template information
        context = template_details(request, 0)
        
        #Make the status add form
        context['status_form'] = StatusCreateForm(initial={'user': request.user})
        if request.method == 'POST':
            status_form = StatusCreateForm(request.POST)
            print(status_form)
            if status_form.is_valid():
                status_form.save()
                return redirect('/')
            
        #Get the user's Status Updates
        context['statuses'] = StatusUpdates.objects.filter(user = request.user)

        #For teachers, get the list of pending registrations
        if (context['role'] == "Teacher"):
            context['pending_registrations'] = Registrations.objects.filter(status = "PENDING")

        #For student, get the list of deadlines
        if (context['role'] == "Student"):
            accepted_registations = Registrations.objects.filter(status = "APPROVED", student = request.user)
            registered_due_dates = Registrations.objects.none()
            for reg in accepted_registations:
                deadlines = CourseDueDates.objects.filter(course_id = reg.course_id)
                registered_due_dates = registered_due_dates | deadlines
            context['duedates'] = registered_due_dates

        return render(request, 'elearning/index.html', context)

# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Account is Disabled")
        else:
            # return HttpResponse("Invalid Login Details")
            print(user)
            return HttpResponseRedirect('/')
    else: 
        return render(request, 'elearning/login.html')
    
# REGISTER A NEW ACCOUNT
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            group = Group.objects.get(name='Student')
            user.groups.add(group)

            registered = True
    else: 
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'elearning/register.html', {'user_form': user_form,
                                                       'profile_form': profile_form,
                                                       'registered': registered})

# CHANGE PASSWORD VIEW
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated')
            return redirect('/')
        else:
            messages.error(request, 'There has been an error')
    else:
        form = PasswordChangeForm(request.user)

    context = template_details(request, 0)
    context["form"] = form
    return render(request, 'elearning/change_password.html', context)

# CHANGE PASSWORD
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

# ADD A NEW COURSE
class CourseCreate(CreateView):
    model = Courses
    template_name = 'elearning/course_add.html'
    form_class = CourseCreateForm
    success_url = "/course_add/" 

    @method_decorator(user_passes_test(is_teacher))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        #Import the base template information
        context=template_details(self.request, 0)
        context = super().get_context_data(**kwargs)
        context['courses'] = Courses.objects.all()
        context['user_image'] = AppUser.objects.get(user = self.request.user).image

        # NEED THESE TO ACCESS ADDITIONAL PAGE INFORMATION
        context['role'] = is_member(self.request.user)
        context['teachers'] = (User.objects.filter(groups__name='Teacher'))
        context['students'] = (User.objects.filter(groups__name='Student'))

        #List of Enrolled Courses for Students
        if (context['role'] == "Student"):
            context['courses_enrolled'] = Registrations.objects.filter(status = "APPROVED", student = self.request.user)
        #

        return context
    
# VIEW THE COURSE INFORMATION
@login_required
def courseView(request, pk):
    #Import the base template information
    context=template_details(request, pk)

    #Information to make the page template display
    context['course_feedback'] = CourseFeedback.objects.filter(course_id=pk)

    #For teachers, get the list of pending registrations on this course
    if (context['role'] == "Teacher"):
        context['pending_registrations'] = Registrations.objects.filter(course = context['selected_course'])
                
    # CALCULATE THE AVERAGE COURSE RATING #
    feedback = context['course_feedback']     
    if (len(feedback) != 0):   
        sum_rating = 0
        for item in feedback:
            sum_rating += item.rating
        average_rating = sum_rating / len(feedback)
        context['average_rating'] = average_rating
    if (len(feedback) == 0): 
        context['average_rating'] = "No Current Ratings"

    #Is the logged in user currently registered for the course?
    if (len(Registrations.objects.filter(student = request.user, course = context['selected_course'])) == 0):
        context['isRegistered'] = "NOT REGISTERED"
    if (len(Registrations.objects.filter(student = request.user, course = context['selected_course'])) != 0):
        context['isRegistered'] = (Registrations.objects.get(student=request.user, course = context['selected_course']).status)

    #Return a form to register as a student
    registerForm = Register_Student_to_CourseForm(initial={'status':'PENDING', 'student': request.user, 'course': context['selected_course']})
    if request.method == 'POST':
        register_form = Register_Student_to_CourseForm(request.POST)
        register_form.save()
        return redirect('/course_view/'+str(pk))

    context['RegisterButton'] = registerForm

    #Return all the course deadlines
    dueDates = CourseDueDates.objects.filter(course_id = context['selected_course'])
    context['dueDates'] = dueDates

    return render(request, 'elearning/course_view.html', context)

# PROFILE PAGES
class UserView(ListView):
    model = User
    template_name = 'elearning/user_view.html'
    success_url = "/user_view"

    @method_decorator(user_passes_test(is_teacher))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        #Import the base template information
        context=template_details(self.request, 0)
        context['users'] = User.objects.all
        context['user_return'] = User.objects.filter(pk=self.kwargs['pk'])[0]
        context['user_return_image'] = AppUser.objects.get(user = context['user_return']).image
        context['user_return_role'] = is_member(context['user_return'])

        context['statuses'] = StatusUpdates.objects.filter(user = context['user_return'])
        context['enrolled_courses'] = Registrations.objects.filter(student = context['user_return'], status = "APPROVED")

        #For student, get the list of deadlines
        registered_due_dates = Registrations.objects.none()
        for reg in context['enrolled_courses']:
            deadlines = CourseDueDates.objects.filter(course_id = reg.course_id)
            registered_due_dates = registered_due_dates | deadlines
        context['due_dates'] = registered_due_dates
        
        print(context['user_return_image'])
        return context

# COURSE ADD FEEDBACK
@login_required
def create_course_feedback_view(request, pk):
    #Import the base template information
    context = template_details(request, pk)

    form = FeedbackCreateForm(initial={'student_id': request.user, 'course_id': context['selected_course'] })

    if request.method == 'POST':
        form = FeedbackCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/course_view/'+str(pk))
    
    context["form"] = form
    return render(request, 'elearning/course_add_feedback.html', context)

# HOME PAGE = CHANGE A PENDING REGISTRATION
@user_passes_test(is_teacher)
def change_registration(request, regpk, status):
    reg_line = Registrations.objects.filter(pk = regpk)[0]
    reg_line.status = status
    reg_line.save()
    return redirect('/')

# COURSE VIEW = CHANGE A PENDING REGISTRATION
@user_passes_test(is_teacher)
def change_registration_cv(request, regpk, status):
    reg_line = Registrations.objects.filter(pk = regpk)[0]
    reg_line.status = status
    reg_line.save()
    return redirect('/course_view/'+str(reg_line.course.pk))

# COURSE ADD DUE DATE
@user_passes_test(is_teacher)
def courseAddDuedate(request, pk):
    #Import the base template information
    context=template_details(request, pk)

    form = AddDueDate(initial={'course_id':context['selected_course']})

    if request.method == 'POST':
        form = AddDueDate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/course_view/'+str(pk))
    
    context['form'] = form
    return render(request, 'elearning/course_add_duedate.html', context)

# COURSE VIEW ALL MATERIAL
@login_required
def courseViewMaterial(request, pk):
    #Import the base template information
    context=template_details(request, pk)

    #Get all the course material
    context['material'] = CourseMaterial.objects.filter(course_id=context['selected_course'])
    return render(request, 'elearning/course_view_material.html', context)

# COURSE ADD MATERIAL
@user_passes_test(is_teacher)
def courseAddMaterial(request, pk):
    #Import the base template information
    context=template_details(request, pk)

    form = AddMaterial(initial={'course_id':context['selected_course']})

    if request.method == 'POST':
        form = AddMaterial(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            form.save()
            return redirect('/course_view_material/'+str(pk))
    
    context['form'] = form
    return render(request, 'elearning/course_add_material.html', context)

# CHAT ROOM
@login_required
def room(request, room_name):
    #Import the base template information
    context=template_details(request, 0)

    context['room_name'] = room_name
    context['messages'] = ChatMessages.objects.filter(room=room_name).order_by('timestamp')

    return render(request, 'elearning/chat.html', context)
