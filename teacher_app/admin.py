from django.contrib import admin
from teacher_app.models import UserProfileInfo, CreateCourse, Comments, Review, SearchModel


class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic', 'type', 'admin_approved']
    list_filter = ['type', 'admin_approved']
    search_fields = ['user__username']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating']
    list_filter = ['user', 'course', 'rating']
    search_fields = ['user__username', 'course__title', 'review_text']
    list_per_page = 10
    ordering = ['-id']


class CreateCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'user', 'type']
    list_filter = ['date', 'user']
    search_fields = ['title', 'user__username']
    list_per_page = 10
    ordering = ['-date']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'user_comments']
    list_filter = ['user', 'course']
    search_fields = ['user__username', 'course__title', 'user_comments']
    list_per_page = 10
    ordering = ['-id']


class SearchModelAdmin(admin.ModelAdmin):
    list_display = ['search_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['search_text']
    list_per_page = 10
    ordering = ['-created_at']


admin.site.register(SearchModel, SearchModelAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(CreateCourse, CreateCourseAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfileInfo, UserProfileInfoAdmin)
