from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('users/', include('apps.users.urls')),
    path('patient/', include('apps.patient.urls')),
    path('prediction/', include('apps.prediction.urls')),
    path('doctor/', include('apps.doctor.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)