import logging
import threading

from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from oneapp.models import Registration
from oneapp.notify_mail import notify_meeting_registration

logger = logging.getLogger(__name__)


def _run_meeting_notify(reg_id: int) -> None:
    connection.close()
    try:
        reg = Registration.objects.get(pk=reg_id)
        notify_meeting_registration(reg)
    except Exception:
        logger.exception("Async meeting registration email failed id=%s", reg_id)
    finally:
        connection.close()


@receiver(post_save, sender=Registration)
def registration_staff_email(sender, instance, created, **kwargs):
    if not created:
        return
    threading.Thread(target=_run_meeting_notify, args=(instance.pk,), daemon=True).start()
