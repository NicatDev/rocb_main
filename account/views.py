from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile 
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfilePictureForm

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, "profile.html", {
        "user": user,
        "profile": profile,
        "form": form
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