from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import api

urlpatterns = [
    path('', login_required(login_url='../login/')(views.index), name='index'),
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'user_login'),
    path('logout/', views.user_logout, name = 'user_logout'),
    path('change_password/', login_required(login_url='../login/')(views.change_password), name='change_password'),
    path('course_add/', views.CourseCreate.as_view(), name = 'course_add'),
    path('course_view/<int:pk>', views.courseView, name = 'course_view'),
    path('course_add_duedate/<int:pk>', views.courseAddDuedate, name = 'course_add_duedate'),
    path('course_add_material/<int:pk>', views.courseAddMaterial, name = 'course_add_material'),
    path('course_view_material/<int:pk>', views.courseViewMaterial, name = 'course_view_material'),
    path('user_view/<int:pk>', views.UserView.as_view(), name = 'user_view'),
    path('feedback_add/<int:pk>', views.create_course_feedback_view, name = 'feedback_add'),
    path('registration_change/<int:regpk>/<str:status>', views.change_registration, name = 'registration_change'),
    path('registration_change_cv/<int:regpk>/<str:status>', views.change_registration_cv, name = 'registration_change_cv'),
    path('chat/<str:room_name>', views.room, name = 'room'),

    path('api/user_details', api.Details.as_view(), name='details_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)