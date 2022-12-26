import random
import string

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields

from apps.auth_manager.models import Account, Developer, User, AccountType, VerifyDetail
from apps.gateway.models import EmailLog

admin.site.register(Account)


# -------------
# Custom User
# -------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("mobile_number", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "mobile_number")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    ADDITIONAL_USER_FIELDS = (
        ("Personal info", {"fields": ["mobile_number"]}),)
    ADD_USER_FIELDS = ((None, {"fields": ["mobile_number", "email"]}),)

    search_fields = ("email", "mobile_number")
    list_display = [
        "id",
        "username",
        "email",
        "mobile_number",
        "first_name",
        "last_name",
        "is_staff",
    ]

    add_fieldsets = ADD_USER_FIELDS + UserAdmin.add_fieldsets
    fieldsets = ADDITIONAL_USER_FIELDS + UserAdmin.fieldsets


class DeveloperResource(resources.ModelResource):
    account = fields.Field(
        column_name='account',
        attribute='account',
        widget=ForeignKeyWidget(Account, 'account')
    )

    def init_instance(self, row, *args, **kwargs):
        try:
            instance = super().init_instance(*args, **kwargs)
            name = row.get("name")
            if name:
                dob = row.get("dob")
                first_name = name.split(' ')[0]
                last_name_list = name.split(' ')[1:4]
                last_name = " ".join(last_name_list)
                fake_number = [str(random.randint(0, 9)) for p in range(0, 11)]
                number = "".join(fake_number)
                username = (first_name + last_name).lower()
                email = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=8))
                user = User.objects.create(
                    first_name=first_name, last_name=last_name, mobile_number=number, email=email, username=username)
                user.set_password('dummy123')
                user.save()
                account_obj, created = Account.objects.get_or_create(
                    user=user, account_type=AccountType.DEVELOPER)
                account_obj.save()
                instance.account = account_obj
                format_str = "%Y-%m-%d %H:%M:%S"
                instance.dob = dob.strptime(str(dob), format_str)
                return instance
        except Exception as e:
            print(row)
            print(e)

    class Meta:
        model = Developer
        widgets = {
            'dob': {'format': '%d/%m/%Y'},
        }


class DeveloperAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DeveloperResource

    list_display = ['pk', 'account', 'dob', 'tech_type']
    search_fields = ['account__user__first_name', 'account__user__last_name']

    class Meta:
        model = Developer
        widgets = {
            'dob': {'format': '%d/%m/%Y'},
        }


class EmailLogAdmin(admin.ModelAdmin):
    class Meta:
        model = EmailLog

    list_display = ['event_name', 'email_from', 'email_to', 'email_sent_at', 'email_status']


class VerifyDetailAdmin(admin.ModelAdmin):
    class Meta:
        model = VerifyDetail

    list_display = ['get_user_name', 'is_verified', 'verify_link_sent_at', 'verified_at']
    search_fields = ['user__first_name', 'user__last_name']
    @admin.display(description='User Name')
    def get_user_name(self, obj):
        return f"{ obj.user.first_name} {obj.user.last_name}"


admin.site.register(Developer, DeveloperAdmin)
admin.site.register(VerifyDetail, VerifyDetailAdmin)
admin.site.register(EmailLog, EmailLogAdmin)
