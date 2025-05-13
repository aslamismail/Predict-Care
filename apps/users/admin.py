from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import CustomUser
from apps.patient.models import MedicalHistory
from apps.doctor.models import Appointment

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('name', 'email', 'profile_picture')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Patient Info', {
            'fields': ('age', 'gender'),
            'classes': ('collapse',),
            'description': 'Fields specific to patients'
        }),
        ('Doctor Info', {
            'fields': ('medical_license_number', 'specialization'),
            'classes': ('collapse',),
            'description': 'Fields specific to doctors'
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

# Medical History Admin
@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'blood_pressure', 'heart_rate', 'smoking_status', 'created_at')
    list_filter = ('smoking_status', 'alcohol_consumption', 'physical_activity_level')
    search_fields = ('patient__username', 'patient__email', 'existing_conditions')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient',)
        }),
        ('Health Indicators', {
            'fields': ('blood_pressure', 'cholesterol_level', 'heart_rate')
        }),
        ('Lifestyle Factors', {
            'fields': ('smoking_status', 'alcohol_consumption', 'physical_activity_level')
        }),
        ('Family History', {
            'fields': (
                'family_history_diabetes', 'family_history_heart_disease',
                'family_history_lungcancer', 'family_history_asthma',
                'family_history_liver_disease', 'family_history_parkinsons'
            )
        }),
        ('Medical Details', {
            'fields': ('existing_conditions', 'current_medications')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('doctor__username', 'patient__username', 'reason')
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('doctor', 'patient', 'date', 'status')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes')
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('doctor', 'patient')

# Admin Site Customization
admin.site.site_header = 'Chronic Disease Prediction Admin'
admin.site.site_title = 'CDP Admin Portal'
admin.site.index_title = 'Welcome to CDP Admin Portal'