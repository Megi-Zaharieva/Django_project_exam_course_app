from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from teacher_app.forms import UserProfileInfoForm, UserForm, ProfileDetailsTeacherForm, AddCourseForm, \
    StudentProfileInfoForm, CommentsForm, ReviewForm, SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from teacher_app.models import UserProfileInfo, CreateCourse, Comments, Review, SearchModel
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Avg


def index(request):
    if not request.user.is_anonymous:
        profile = User.objects.get(pk=request.user.pk)
        profile_info = UserProfileInfo

        context = {
            'profile_info': profile_info,
            'profile': profile,
        }
        return render(request, 'basic_app/index.html', context)
    else:
        return render(request, 'basic_app/index.html')


class UserRegisterView(View):
    registered = False

    def get(self, request):
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'basic_app/registration.html', context)

    def post(self, request):
        registered = False

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password'])
            login(request, user)

            registered = True

            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered
            }
            return render(request, 'basic_app/index.html', context)

        else:
            context = {'user_form': user_form,
                       'profile_form': profile_form,
                       }
            return render(request, 'basic_app/registration.html', context)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'basic_app/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('index')
        else:
            context = {
                'error': 'Invalid User/Password!'
            }
            return render(request, 'basic_app/login.html', context)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.clear()
        return redirect('index')


@login_required
def profile_details(request):
    user = request.user
    user_profile = UserProfileInfo.objects.get(user=user)
    user_type = user_profile.type

    if request.method == 'POST':
        if user_type == "Student":
            user_form = UserForm(request.POST, instance=user)
            profile_form = StudentProfileInfoForm(request.POST, request.FILES, instance=user_profile)
        else:
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileDetailsTeacherForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        user_form = UserForm(instance=user)
        if user_type == "Student":
            profile_form = StudentProfileInfoForm(instance=user_profile)
        else:
            profile_form = ProfileDetailsTeacherForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_type': user_type,
    }
    return render(request, 'basic_app/profile_details.html', context)


class TeachersHomeView(TemplateView):
    template_name = 'basic_app/teachers/home.html'


class TeacherCoursesView(View):
    def get(self, request):
        user = request.user
        courses_list = CreateCourse.objects.filter(user=user)

        context = {
            'courses_list': courses_list
        }
        return render(request, 'basic_app/teachers/course_list.html', context)


class AddCourseView(View):
    def get(self, request):
        form = AddCourseForm()
        context = {
            'form': form
        }
        return render(request, 'basic_app/teachers/add-course.html', context)

    def post(self, request):
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user

            if 'course_image_url' in request.FILES:
                course.course_image_url = request.FILES['course_image_url']

            course.save()
            return redirect('teacher_app:my_courses')

        context = {
            'form': form
        }
        return render(request, 'basic_app/teachers/add-course.html', context)


class CourseDetailsView(View):
    template_name = 'basic_app/teachers/course-details.html'

    def get(self, request, course_id):
        form = get_object_or_404(CreateCourse, id=course_id)
        video_url = form.video_url
        video_url_split = video_url.split("=")
        video_id = video_url_split[1]
        video_details = YoutubeVideoUrl(video_id)
        comments_ls = Comments.objects.filter(course_id=course_id).order_by('-id')
        course_id = form.id
        user_has_review = Review.objects.filter(course_id=course_id, user=request.user).exists()

        context = {
            'video_details': video_details,
            'form': form,
            'comments_ls': comments_ls,
            'course_id': course_id,
            'user_has_review': user_has_review,
        }
        return render(request, self.template_name, context)


def YoutubeVideoUrl(video_id):
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return embed_url


class EditCourseView(View):
    template_name = 'basic_app/teachers/course-edit.html'

    def get(self, request, course_id):

        if request.user.is_superuser or request.user.is_staff:
            course = get_object_or_404(CreateCourse, id=course_id)
        else:
            course = get_object_or_404(CreateCourse, id=course_id, user=request.user)

        form = AddCourseForm(instance=course)
        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        if request.user.is_superuser or request.user.is_staff:
            course = get_object_or_404(CreateCourse, id=course_id)
        else:
            course = get_object_or_404(CreateCourse, id=course_id, user=request.user)

        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.date = timezone.now().date()
            course.save()
            return redirect('teacher_app:course_details', course_id=course.id)
        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)


class DeleteCourseView(View):
    def test_func(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)
        return self.request.user == course.user or self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)

        context = {
            'course': course
        }
        return render(request, 'basic_app/teachers/course-delete.html', context)

    def post(self, request, course_id):
        course = get_object_or_404(CreateCourse, id=course_id)

        if self.test_func(request, course_id):
            course.delete()
            return redirect('teacher_app:my_courses')
        else:
            return render(request, 'basic_app/teachers/access_denied.html')


class ListAllTeachersView(View):
    def get(self, request):
        teachers_list = UserProfileInfo.objects.filter(type='Teacher', user__is_active=True, admin_approved='Yes')

        context = {
            'teachers_list': teachers_list
        }
        return render(request, 'basic_app/students/teachers_list.html', context)


def TeacherCoursesAndDetailsView(request, teacher_id):
    teacher = UserProfileInfo.objects.get(id=teacher_id)
    courses_list = CreateCourse.objects.filter(user=teacher.user)

    for course in courses_list:
        course.average_rating = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg']

    Context = {
        'teacher': teacher,
        'courses_list': courses_list
    }
    return render(request, 'basic_app/teachers/course_list.html', Context)


def AddEditComment(request, course_id, comment_id=None):
    user = request.user
    course = get_object_or_404(CreateCourse, id=course_id)

    if comment_id:
        comment = get_object_or_404(Comments, id=comment_id)
    else:
        comment = None

    if request.method == 'POST':
        form = CommentsForm(request.POST, instance=comment)

        if form.is_valid():
            user_comment = form.save(commit=False)
            user_comment.course = course
            user_comment.user = user
            user_comment.save()

            return redirect('teacher_app:course_details', course_id=course_id)
    else:
        form = CommentsForm(instance=comment)

    context = {
        'form': form,
        'course': course,
        'comment': comment,
    }
    return render(request, 'basic_app/comments/add_edit_comment.html', context)


class DeleteCommentView(UserPassesTestMixin, View):
    template_name = 'basic_app/comments/delete_comment.html'

    def test_func(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comments, id=comment_id)
        return self.request.user == comment.user or self.request.user.is_superuser or self.request.user.is_staff

    def post(self, request, course_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id, course_id=course_id)

        if self.test_func():
            comment.delete()
            return redirect('teacher_app:course_details', course_id=course_id)
        else:
            return HttpResponseForbidden("You are not allowed to delete this comment.")

    def get(self, request, course_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id, course_id=course_id)

        if self.test_func():
            course = get_object_or_404(CreateCourse, id=course_id)
            context = {
                'course': course,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseForbidden("You are not allowed to delete this comment.")


class AddReviewView(View):
    template_name = 'basic_app/comments/add_review.html'

    def get(self, request, course_id):
        form = ReviewForm()

        context = {
            'form': form,
            'course_id': course_id
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        form = ReviewForm(request.POST)
        course = get_object_or_404(CreateCourse, id=course_id)
        existing_review = Review.objects.filter(course=course, user=request.user).first()
        if existing_review:
            return redirect('teacher_app:view_reviews', course_id=course_id)

        if form.is_valid():
            review = form.save(commit=False)
            review.course = CreateCourse.objects.get(id=course_id)
            review.user = request.user
            review.save()
            return redirect('teacher_app:view_reviews', course_id=course_id)

        context = {
            'form': form,
            'course_id': course_id
        }
        return render(request, self.template_name, context)


class ViewReviews(View):
    template_name = 'basic_app/comments/view_reviews.html'

    def get(self, request, course_id):
        reviews = Review.objects.filter(course_id=course_id)
        user_has_review = Review.objects.filter(course_id=course_id, user=request.user).exists()

        if user_has_review:
            messages.error(request, 'Review already added.')

        context = {
            'reviews': reviews,
            'course_id': course_id,
            'user_has_review': user_has_review
        }
        return render(request, self.template_name, context)


class SearchView(View):
    template_name = 'basic_app/comments/search_results.html'

    def get(self, request):
        form = SearchForm()

        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            SearchModel.objects.create(search_text=search_text)
            courses_ls = CreateCourse.objects.filter(title__icontains=search_text)

            context = {
                'form': form,
                'courses_ls': courses_ls,
                'search_button_clicked': True
            }
            return render(request, self.template_name, context)

        context = {
            'form': form,
            'search_button_clicked': False
        }
        return render(request, self.template_name, context)


def contacts_view(request):
    return render(request, 'basic_app/contacts.html')


def custom_page_not_found(request, *args, **kwargs):
    return render(request, 'basic_app/404.html')
