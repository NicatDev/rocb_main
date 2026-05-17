from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext as _
from .forms import ProfileEditForm, ProfilePictureForm


@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        action = request.POST.get('action', 'save_details')

        if action == 'remove_picture':
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)
            profile.profile_picture = None
            profile.save(update_fields=['profile_picture'])
            messages.success(request, _('Profile picture removed.'))
            return redirect('profile_view')

        if action == 'upload_avatar':
            pic_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
            if pic_form.is_valid():
                pic_form.save()
                messages.success(request, _('Profile picture updated.'))
            else:
                messages.error(request, _('Could not upload image. Please use JPEG, PNG, or WebP.'))
            return redirect('profile_view')

        form = ProfileEditForm(request.POST, request.FILES, user=user, profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile saved successfully.'))
            return redirect('profile_view')
        messages.error(request, _('Please correct the errors below.'))
    else:
        form = ProfileEditForm(user=user, profile=profile)

    avatar_initials = ''
    if user.first_name:
        avatar_initials += user.first_name[0].upper()
    if user.last_name:
        avatar_initials += user.last_name[0].upper()
    if not avatar_initials and user.username:
        avatar_initials = user.username[0].upper()

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'form': form,
        'avatar_initials': avatar_initials,
    })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def logout_url_view(request):
    logout(request)
    return redirect("home")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("rememberme")
        next_url = request.POST.get("next")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    response = render(request, "login.html")
    
    # Explicitly delete messages from session (optional)
    list(messages.get_messages(request))  # iterating clears them
    return response

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from .models import Profile
from django.contrib.auth import login

def register_view(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        phone_number = request.POST.get("phone_number")
        organization = request.POST.get("organization")
        position = request.POST.get("position")
        # Validate passwords
        if password1 != password2:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        user.is_active = False
        user.save()

        # Create profile with additional fields
        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            organization=organization,
            position=position
        )


        return JsonResponse({
            "status": "success",
            "message": "Your registration has been successfully submitted! It will be reviewed by an administrator shortly."
        })

    return render(request, "register.html")

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def pending_approvals_view(request):
    # DƏYİŞİKLİK: Yalnız statusu "pending" olanları göstər
    pending_users = User.objects.filter(profile__status='pending', is_active=False).order_by('-date_joined')
    context = {
        'pending_users': pending_users
    }
    return render(request, 'pending_approvals.html', context)

@login_required
@user_passes_test(is_staff)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # İstifadəçini aktiv et
    user.is_active = True
    user.save()
    
    # DƏYİŞİKLİK: Profil statusunu "approved" et
    user.profile.status = 'approved'
    user.profile.save()
    
    messages.success(request, f"User '{user.username}' has been approved.")
    return redirect('pending_approvals')

@login_required
@user_passes_test(is_staff)
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    
    # DƏYİŞİKLİK: İstifadəçini silmək əvəzinə, profil statusunu "rejected" et
    # user.delete()  <-- BU SƏTRİ SİLİN VƏ YA KOMMENTƏ ALIN
    user.profile.status = 'rejected'
    user.profile.save()
    
    messages.warning(request, f"User '{username}' has been rejected.")
    return redirect('pending_approvals')