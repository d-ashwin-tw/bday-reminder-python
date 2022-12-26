from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.auth_manager.models import User, Account, Developer


@receiver(pre_save, sender=User)
def save_user_email_as_lowercase(sender, instance: User, *args, **kwargs):
    """
    When user signup or update the user model from admin. The email should always save as lowercase
    """
    instance.email = instance.email.lower()


# @receiver(post_save, sender=User)
# def after_signup_01(sender, instance, created, **kwargs):
#     if created:
#         try:
#             account_obj = Account.objects.create(user=instance)
#         except Exception as e:
#             print(e)
#     return


# @receiver(post_save, sender=Account)
# def after_signup_02(sender, instance, created, **kwargs):
#     if created:
#         try:
#             model1_obj = Developer.objects.create(account=instance,dob="")
#         except Exception as e:
#             print(e)
#     return
