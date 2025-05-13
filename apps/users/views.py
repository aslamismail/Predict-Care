from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PatientProfileForm, DoctorProfileForm
from django.contrib import messages
from django.contrib.auth import logout

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, PatientProfileForm, DoctorProfileForm, CustomUserChangeForm
from django.contrib.auth import login

def register_user(request):
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debugging line
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            print(f"User type: {user_type}")  # Debugging line
            
            # Initialize profile form based on user type
            if user_type == 'patient':
                profile_form = PatientProfileForm(request.POST)
            elif user_type == 'doctor':
                profile_form = DoctorProfileForm(request.POST)
            else:
                profile_form = None

            # Validate and save profile form
            if profile_form and profile_form.is_valid():
                print("Profile form is valid")
                for field in ['age', 'gender', 'medical_license_number', 'specialization', 'height', 'weight', 'bmi']:
                    setattr(user, field, profile_form.cleaned_data.get(field))
                user.save()
                messages.success(request, "Registration successful!")
            else:
                print("Profile form errors:", profile_form.errors if profile_form else "No form")

            # Log in the user and redirect
            login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # Debugging line
           # messages.error(request, ".")

            all_errors = ' '.join(
                error for errors in form.errors.values() for error in errors
            )

            messages.error(request, "Registration failed: "+ all_errors)
    
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)

        if user.is_patient():
            profile_form = PatientProfileForm(request.POST, instance=user)
        elif user.is_doctor():
            profile_form = DoctorProfileForm(request.POST, instance=user)
        else:
            profile_form = None

        if form.is_valid() and (profile_form is None or profile_form.is_valid()):
            form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check your inputs.")

    return redirect('profile')