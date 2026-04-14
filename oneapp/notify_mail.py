"""
Staff notification emails (meeting registration, etc.).
Configure EMAIL_HOST_USER / EMAIL_HOST_PASSWORD and ROCB_NOTIFY_STAFF_EMAILS in project/settings.py.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_staff_mail(subject: str, message: str) -> None:
    user = getattr(settings, "EMAIL_HOST_USER", "") or ""
    password = getattr(settings, "EMAIL_HOST_PASSWORD", "") or ""
    if not user or not password:
        logger.warning("Email credentials not configured; skipping: %s", subject)
        return
    recipients = list(getattr(settings, "ROCB_NOTIFY_STAFF_EMAILS", []) or [])
    if not recipients:
        logger.warning("ROCB_NOTIFY_STAFF_EMAILS empty; skipping: %s", subject)
        return
    try:
        send_mail(
            subject=subject[:998],
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send staff email: %s", subject)


def notify_meeting_registration(registration) -> None:
    """Notify staff when someone registers via meeting registration form."""
    topic = (registration.subject or "").strip() or registration.full_name or "Meeting registration"
    subject = f"[ROCB Europe] Meeting registration: {topic}"
    lines = [
        "New meeting registration",
        "",
        f"Registration ID: {registration.id}",
        f"Full name: {registration.full_name}",
        f"Phone: {registration.phone_number}",
        f"Email: {registration.email}",
        f"Subject / topic: {registration.subject or '—'}",
        f"Position: {registration.position or '—'}",
        f"Organization: {registration.organization or '—'}",
        f"Note: {registration.note or '—'}",
    ]
    send_staff_mail(subject, "\n".join(lines))
