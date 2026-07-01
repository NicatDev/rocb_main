import json

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext as _
from .forms import ProfileEditForm, ProfilePictureForm, ChangePasswordForm


PROFILE_FIELD_CONFIG = {
    'first_name': {'target': 'user', 'attr': 'first_name', 'form_field': 'first_name'},
    'last_name': {'target': 'user', 'attr': 'last_name', 'form_field': 'last_name'},
    'email': {'target': 'user', 'attr': 'email', 'form_field': 'email'},
    'phone_number': {'target': 'profile', 'attr': 'phone_number', 'form_field': 'phone_number'},
    'organization': {'target': 'profile', 'attr': 'organization', 'form_field': 'organization'},
    'position': {'target': 'profile', 'attr': 'position', 'form_field': 'position'},
    'birth_date': {'target': 'profile', 'attr': 'birth_date', 'form_field': 'birth_date'},
}


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

    field_values = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': profile.phone_number,
        'organization': profile.organization,
        'position': profile.position,
        'birth_date': profile.birth_date.isoformat() if profile.birth_date else '',
    }

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'form': form,
        'avatar_initials': avatar_initials,
        'field_values': field_values,
    })


@login_required
@require_POST
@csrf_protect
def profile_field_update(request):
    """Save a single profile field (AJAX from profile page)."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    try:
        if request.content_type and 'application/json' in request.content_type:
            payload = json.loads(request.body.decode('utf-8'))
            field_name = payload.get('field')
            raw_value = payload.get('value', '')
        else:
            field_name = request.POST.get('field')
            raw_value = request.POST.get('value', '')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'message': _('Invalid request.')}, status=400)

    if field_name not in PROFILE_FIELD_CONFIG:
        return JsonResponse({'success': False, 'message': _('Unknown field.')}, status=400)

    config = PROFILE_FIELD_CONFIG[field_name]
    form = ProfileEditForm(user=user, profile=profile)
    form_field = form.fields[config['form_field']]

    if raw_value in (None, ''):
        cleaned = '' if form_field.required is False else None
        if form_field.required:
            return JsonResponse(
                {'success': False, 'message': _('This field is required.')},
                status=400,
            )
    else:
        try:
            cleaned = form_field.clean(raw_value)
        except forms.ValidationError as exc:
            return JsonResponse(
                {'success': False, 'message': '; '.join(exc.messages)},
                status=400,
            )

    if config['target'] == 'user':
        if cleaned == '' and not form_field.required:
            setattr(user, config['attr'], '')
        else:
            setattr(user, config['attr'], cleaned)
        user.save(update_fields=[config['attr']])
        display_value = getattr(user, config['attr']) or ''
    else:
        setattr(profile, config['attr'], cleaned if cleaned != '' else None)
        profile.save(update_fields=[config['attr']])
        val = getattr(profile, config['attr'])
        if field_name == 'birth_date' and val:
            display_value = val.isoformat()
        else:
            display_value = val or ''

    return JsonResponse({'success': True, 'field': field_name, 'value': display_value})


@login_required
@require_POST
@csrf_protect
def change_password_view(request):
    """Change password (AJAX modal or standard POST)."""
    form = ChangePasswordForm(user=request.user, data=request.POST)
    is_ajax = (
        request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        or 'application/json' in (request.content_type or '')
    )

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        message = _('Password updated successfully.')
        if is_ajax:
            return JsonResponse({'success': True, 'message': message})
        messages.success(request, message)
        return redirect('profile_view')

    errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
    first_error = next((msgs[0] for msgs in errors.values() if msgs), _('Please correct the errors below.'))

    if is_ajax:
        return JsonResponse(
            {'success': False, 'message': first_error, 'errors': errors},
            status=400,
        )

    messages.error(request, first_error)
    return redirect('profile_view')


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