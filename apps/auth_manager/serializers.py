from dataclasses import field
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.auth_manager.models import User, Developer, Account, VerifyDetail


class DeveloperRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.CharField(required=True, label="Email")
    password = serializers.CharField(max_length=50, label="Password")
    dob = serializers.DateField(
        required=False, format="%d-%m-%Y", label="Date of Birth"
    )
    mobile_number = serializers.CharField(required=True, label="Mobile Number")
    name = serializers.CharField(required=True, label="Name")

    class Meta:
        model = User
        fields = ['dob', 'name', 'username',
                  'mobile_number', 'email', 'password']

    def save(self, **kwargs):
        try:
            user = User()
            username = self.validated_data.get("username", "")
            user.username = username
            user.first_name = self.validated_data.get("name", "")
            user.last_name = self.validated_data.get("last_name", "")
            user.email = self.validated_data.get("email", "")
            user.mobile_number = self.validated_data.get("mobile_number")
            user.set_password(self.validated_data.get("password", ""))
            user.save()
            # Create Account
            account_obj = Account.objects.create(user=user)

            # Create Developer
            dob = self.validated_data.get("dob")
            developer_obj = Developer.objects.create(
                account=account_obj, dob=dob)
            return user
        except Exception as e:
            print(e)


class DeveloperListSerializer(serializers.ModelSerializer):
    tech_type = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_detail_verified = serializers.SerializerMethodField()

    class Meta:
        model = Developer
        fields = ['pk', 'username', 'email',
                  'first_name','last_name','mobile_number', 'dob', 'tech_type', 'is_detail_verified']

    def get_tech_type(self, obj):
        return str(obj.tech_type.name)
    def get_first_name(self, obj):
        return str(obj.account.user.first_name)
    def get_last_name(self, obj):
        return str(obj.account.user.last_name)
    def get_username(self, obj):
        return str(obj.account.user.username)

    def get_email(self, obj):
        return str(obj.account.user.email)

    def get_mobile_number(self, obj):
        return str(obj.account.user.mobile_number)

    def get_is_detail_verified(self, obj):
        result = False
        vd = VerifyDetail.objects.filter(user=obj.account.user).last()
        if vd:
            if vd.is_verified:
                result = True
            else:
                result = False
        return str(result)


class DeveloperUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['dob', 'tech_type']


class LoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField(
        required=True, label="Email / Mobile")
    password = serializers.CharField(required=True, label="Password")


class DeveloperDeleteSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    class Meta:
        model = Developer
        fields = ['pk']

    def validate(self, data):
        user_id = data.get('pk')
        if not Developer.objects.filter(account__user__is_active=True, pk=user_id):
            raise serializers.ValidationError("Developer id not exists")
        return data

    def save(self, **kwargs):
        try:
            user_id = self.data.get('pk')
            instance = Developer.objects.filter(pk=user_id).last()
            instance.account.user.is_active=False
            instance.account.user.save()
            return instance
        except Exception as e:
            print(e)
