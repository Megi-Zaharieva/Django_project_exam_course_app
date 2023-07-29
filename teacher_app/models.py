from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from datetime import date

User_model = get_user_model()


class UserProfileInfo(models.Model):
    CHOICES = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    ]
    APPROVE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=800)
    type = models.CharField(blank=False, null=False, choices=CHOICES)
    file = models.FileField(blank=True, null=True, upload_to='user_files')
    admin_approved = models.CharField(blank=True, null=True, choices=APPROVE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True,)

    def __str__(self):
        return self.user.username


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic', 'file', 'type', 'admin_approved']
    fields = ['user', 'profile_pic', 'file', 'type', 'admin_approved']


class CreateCourse(models.Model):

    CHOICES = [
        ('Math 1', 'Math 1'),
        ('Math 2', 'Math 2'),
        ('Math 3', 'Math 3'),
        ('Math 4', 'Math 4'),
        ('Math 5', 'Math 5'),
        ('Math 6', 'Math 6'),
        ('Math 7', 'Math 7'),
        ('Math 8', 'Math 8'),
        ('Math 9', 'Math 9'),
        ('Math 10', 'Math 10'),
        ('Math 11', 'Math 11'),
        ('Math 12', 'Math 12')
    ]

    title = models.CharField(blank=False, null=False, max_length=255)
    video_url = models.URLField(default=None)
    course_image_url = models.URLField(null=True, blank=True)
    date = models.DateField(default=date.today())
    type = models.CharField(blank=False, null=False, choices=CHOICES)
    description = models.TextField(blank=True, null=True, max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comments(models.Model):
    course = models.ForeignKey(CreateCourse, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comments = models.TextField(blank=False, null=False, max_length=250)

    def __str__(self):
        return f"Comments by {self.user.username} for {self.course.title}"


class Review(models.Model):

    CHOICE_REVIEW = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    course = models.ForeignKey(CreateCourse, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    review_text = models.TextField(blank=True, null=True, max_length=300)
    rating = models.IntegerField(choices=CHOICE_REVIEW)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"


class SearchModel(models.Model):
    search_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_text