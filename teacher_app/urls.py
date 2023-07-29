from django.contrib.auth.decorators import login_required
from django.urls import path
from teacher_app import views
from teacher_app.views import UserLoginView, UserRegisterView, TeacherCoursesView, AddCourseView, \
    CourseDetailsView, EditCourseView, DeleteCourseView, ListAllTeachersView, TeachersHomeView

app_name = 'teacher_app'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('user_login/', UserLoginView.as_view(), name='login'),
    path('profile/details', views.profile_details, name='profile_details'),
    path('teachers/home/', login_required(TeachersHomeView.as_view()), name='teachers_home'),
    path('teachers/my_courses/', login_required(TeacherCoursesView.as_view()), name='my_courses'),
    path('teachers/add_course/', login_required(AddCourseView.as_view()), name='add_course'),
    path('course/details/<int:course_id>/', login_required(CourseDetailsView.as_view()), name='course_details'),
    path('course/edit/<int:course_id>/', login_required(EditCourseView.as_view()), name='edit_course'),
    path('course/delete/<int:course_id>/', login_required(DeleteCourseView.as_view()), name='delete_course'),
    path('teachers_list/', login_required(ListAllTeachersView.as_view()), name='teachers_list'),
    path('teacher/<int:teacher_id>/courses/', login_required(views.TeacherCoursesAndDetailsView),
         name='teacher_courses_list'),
    path('course/<int:course_id>/add_comment/', login_required(views.AddEditComment), name='add_comment'),
    path('course/<int:course_id>/edit_comment/<int:comment_id>/', login_required(views.AddEditComment),
         name='edit_comment'),
    path('course/<int:course_id>/delete_comment/<int:comment_id>/', login_required(views.DeleteCommentView.as_view()),
         name='delete_comment'),
    path('course/<int:course_id>/add_review/', login_required(views.AddReviewView.as_view()), name='add_review'),
    path('view_reviews/<int:course_id>', login_required(views.ViewReviews.as_view()), name='view_reviews'),
    path('search/', login_required(views.SearchView.as_view()), name='search_results'),
    path('contacts/', views.contacts_view, name='contacts'),
]
