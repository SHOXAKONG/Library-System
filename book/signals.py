from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import FileUpload

@receiver(post_save, sender=FileUpload)
def send_upload_notification(sender, instance, created, **kwargs):
    if created:
        subject = "Uploaded New File"
        message = f"Your {instance.title} Uploaded Successfully"
        from_email = 'bekmurodovshohruh0224@gmail.com'
        recipient_list = [instance.user.email]

        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False,
        )