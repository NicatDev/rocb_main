from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Profile 
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = None
    return render(request, "profile.html", {"user": user, "profile": profile})

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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
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

        # Create profile with additional fields
        Profile.objects.create(
            user=user,
            phone_number=phone_number,
            organization=organization,
            position=position
        )


        return JsonResponse({"success": "User registered successfully", 'status':'success'})

    return render(request, "register.html")
