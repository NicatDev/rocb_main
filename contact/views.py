from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ContactInfo, Contact
from .forms import ContactForm
from about.models import About


@require_http_methods(["GET", "POST"])
def contact_view(request):
    # ContactInfo modelinden data götürülecek
    contact_infos = ContactInfo.objects.all()
    tabs = About.objects.order_by('created_at')

    if request.method == 'POST':
        form = ContactForm(request.POST)

        # AJAX request üçün
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if form.is_valid():
                try:
                    # Form datasını al
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    subject = form.cleaned_data['subject']
                    message = form.cleaned_data['message']
                    address = form.cleaned_data.get('address', '')

                    # Email subject və message hazırla
                    email_subject = f"New Contact Form Submission: {subject}"
                    email_message = f"""
                    New contact form submission:
                    
                    Name: {name}
                    Email: {email}
                    Phone: {phone}
                    Address: {address}
                    Subject: {subject}
                    
                    Message:
                    {message}
                    """

                    # HTML email template
                    try:
                        html_content = render_to_string('emails/contactform.html', {
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'address': address,
                            'subject': subject,
                            'message': message
                        })
                    except:
                        html_content = None

                    # Form datasını database-ə yadda saxla
                    form.save()

                    # Email göndər
                    send_mail(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],  # Admin email-ə göndər
                        html_message=html_content,
                        fail_silently=False,
                    )

                    return JsonResponse({
                        'success': True,
                        'message': 'Your message has been sent successfully!'
                    })

                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'message': 'There was an error sending your message. Please try again.',
                        'error': str(e)
                    }, status=500)
            else:
                # Form validation errors
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                }, status=400)

        # Normal form submission (non-AJAX)
        else:
            if form.is_valid():
                try:
                    # Form datasını al
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    subject = form.cleaned_data['subject']
                    message = form.cleaned_data['message']
                    address = form.cleaned_data.get('address', '')

                    # Email subject və message hazırla
                    email_subject = f"New Contact Form Submission: {subject}"
                    email_message = f"""
                    New contact form submission:
                    
                    Name: {name}
                    Email: {email}
                    Phone: {phone}
                    Address: {address}
                    Subject: {subject}
                    
                    Message:
                    {message}
                    """

                    # HTML email template
                    try:
                        html_content = render_to_string('emails/contactform.html', {
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'address': address,
                            'subject': subject,
                            'message': message
                        })
                    except:
                        html_content = None

                    # Form datasını database-ə yadda saxla
                    form.save()

                    # Email göndər
                    send_mail(
                        email_subject,
                        email_message,
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],  # Admin email-ə göndər
                        html_message=html_content,
                        fail_silently=False,
                    )

                    messages.success(
                        request, 'Your message has been sent successfully!')
                    return redirect('contact')

                except Exception as e:
                    messages.error(
                        request, 'There was an error sending your message. Please try again.')
            else:
                messages.error(
                    request, 'Please correct the errors in the form.')

    else:
        form = ContactForm()

    context = {
        'form': form,
        'contact_infos': contact_infos,
        'tabs': tabs
    }

    return render(request, 'contact.html', context)
