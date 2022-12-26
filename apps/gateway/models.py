from django.db import models

# Create your models here.


class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    html_content = models.TextField()

    def __str__(self):
        return self.template_name


class EmailLog(models.Model):
    EMAIL_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ERROR', 'error'),
        ('DELIVERED', 'delivered'),
    )
    event_name = models.CharField(max_length=255, blank=True, null=True)
    email_from = models.EmailField()
    email_to = models.EmailField()
    email_sent_at = models.DateTimeField()
    email_status = models.CharField(max_length=20,
                                    choices=EMAIL_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return str(self.email_to)
