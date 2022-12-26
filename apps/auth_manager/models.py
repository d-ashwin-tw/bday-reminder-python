
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from enumfields import EnumField
from enum import Enum

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
class User(AbstractUser):
    mobile_number = models.CharField(
        max_length=40, unique=True, blank=False, null=False, db_index=True
    )
    REQUIRED_FIELDS = ["mobile_number", "email"]

    def __str__(self):
        return f"{self.mobile_number}/{self.email}"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountType(Enum):
    TEAM_LEAD = "TeamLead"
    DEVELOPER = "Developer"


class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    account_type = EnumField(AccountType, max_length=15,
                             default=AccountType.DEVELOPER)

    def __str__(self):
        return f"{self.user.first_name}-{self.user.last_name}"


class TechType(Enum):
    PYTHON = "PYTHON"


class Developer(BaseModel):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, db_index=True)
    
    dob = models.DateField(blank= True,null=True)

    # dob = models.DateField(blank=True, null=False,default='')
    tech_type = EnumField(TechType, max_length=15, default=TechType.PYTHON)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='')
    doj = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.account)


class VerifyDetail(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verify_link_sent_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return int(self.id)
