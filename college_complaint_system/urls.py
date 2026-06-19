from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('complaints.urls')),
    path('complaints/', include('complaints.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='complaints/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )