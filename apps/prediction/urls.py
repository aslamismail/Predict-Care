from django.urls import path
from . import views
from .views import prediction_detail
from .views import get_patients

app_name = 'prediction'

urlpatterns = [
    path('dashboard/', views.disease_prediction_dashboard, name='dashboard'),
    path('predict/<str:disease_type>/', views.predict_disease_risk, name='predict_disease'),
    path('prediction/<int:prediction_id>/', prediction_detail, name='prediction_detail'),
    path('api/get-patients/', get_patients, name='get_patients'),
]
