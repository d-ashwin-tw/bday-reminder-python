# django LIB
from django.utils import timezone
from string import Template

from django.core.mail import EmailMultiAlternatives

from apps.gateway.models import EmailTemplate, EmailLog


def send_email(**kwargs):
    try:
        from_email = kwargs.get("from_email")
        to_emails = kwargs.get("to_emails")
        template_name = kwargs.get("template_name")
        extra_params = kwargs.get("extra_params")

        # Create the email log object with default status as pending before sending mail
        em = EmailLog.objects.create(event_name=template_name, email_from=from_email, email_to=to_emails, email_sent_at=timezone.now())
        subject, message = get_subject_and_message(template_name, extra_params)
        msg = EmailMultiAlternatives(subject, message, from_email, to_emails)
        msg.attach_alternative(message, "text/html")
        msg.send(fail_silently=False)

        # Update the email log object
        em.email_status="DELIVERED"
        em.save()
    except Exception as e:
        print(e)


def get_subject_and_message(template_name, extra_params):
    subject, message = "Test", "testing"
    try:
        email_template = EmailTemplate.objects.get(template_name=template_name)
        subject = email_template.subject.format()
        template = Template(email_template.html_content)
        message = template.substitute(**extra_params)
    except Exception as e:
        print(e)
    return subject, message


