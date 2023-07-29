from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from teacher_app import views
from teacher_app.views import UserLogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('teacher_app/', include('teacher_app.urls')),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('404/', views.custom_page_not_found, name='error')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'teacher_app.views.custom_page_not_found'
