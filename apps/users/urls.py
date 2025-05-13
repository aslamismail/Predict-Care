from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile, edit_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('custom-logout/', views.custom_logout, name='custom_logout'),
    path('edit-profile/', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
