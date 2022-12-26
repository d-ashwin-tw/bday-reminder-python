from django.contrib.auth import get_user_model, login, authenticate
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions, generics, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth_manager.common_helper import response_data
from apps.auth_manager.models import Account, Developer, VerifyDetail
from apps.auth_manager.serializers import DeveloperRegisterSerializer, DeveloperListSerializer, \
    DeveloperUpdateSerializer, LoginSerializer, DeveloperDeleteSerializer
from apps.gateway import gateway_email
from birthday_reminder.settings import BACKEND_URL

User = get_user_model()


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                email_or_mobile = request.data.get('email_or_mobile')
                user = User.objects.filter(Q(email=email_or_mobile) | Q(
                    mobile_number=email_or_mobile)).last()
                if user:
                    auth_user = authenticate(
                        username=user.username, password=data["password"]
                    )
                    login(request, auth_user,
                          backend="django.contrib.auth.backends.ModelBackend")
                    return response_data(200, "success", data={}, errors=None)
                else:
                    return response_data(400, "Failed", data={}, errors="User not found")
            else:
                return response_data(400, "Failed", data={}, errors=serializer.errors)
        except Exception as e:
            return response_data(500, str(e), data={}, errors=None)


class AddDeveloper(generics.CreateAPIView):
    serializer_class = DeveloperRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                # serializer.save()
                to_emails = ["ashwin@thoughtwin.com"]
                from_email = "ashwin@thoughtwin.com"
                extra_params = {}
                extra_params['name'] = 'Syed Rizvi'
                gateway_email.send_email(
                    from_email=from_email,
                    to_emails=to_emails,
                    template_name="BIRTHDAY",
                    extra_params=extra_params
                )
                return response_data(200, "success", data={}, errors=None)
            else:
                return response_data(400, serializer.errors, data={}, errors=None)
        except Exception as e:
            print(e)


class ListDeveloper(generics.ListAPIView):
    serializer_class = DeveloperListSerializer
    def get_queryset(self):
        queryset = Developer.objects.filter(account__user__is_active=True).order_by('-dob')
        if self.request.GET.get("is_active", None) == 'false':
            queryset = Developer.objects.filter(account__user__is_active=False).order_by('-dob')
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            data = serializer.data
            message = "success"
            return response_data(200, message, data=data, errors=None)
        except Exception as e:
            message = str(e)
            return response_data(500, message, data=None, errors=None)


class UpdateDeveloper(generics.UpdateAPIView):
    serializer_class = DeveloperUpdateSerializer
    queryset = Developer.objects.all()

    def update(self, request, developer_id=None, *args, **kwargs):
        message = "Failed"
        try:
            obj = Developer.objects.filter(pk=developer_id).last()
            serializer = self.get_serializer(instance=obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                message = "success"
                return response_data(200, message, data={}, errors=None)
            else:
                message = serializer.errors
                return response_data(400, message, data={}, errors=None)
        except Exception as e:
            errors = str(e)
            return response_data(500, message, data={}, errors=errors)


class ListDeveloperTest(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            return Response({"testing": "done"})
        except Exception as e:
            return Response({"error": str(e)})


class DeactivateDeveloper(generics.CreateAPIView):
    serializer_class = DeveloperDeleteSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return response_data(200, "success", data={}, errors=None)
            else:
                return response_data(400, serializer.errors, data={}, errors=None)
        except Exception as e:
            return response_data(500, "failed", data={}, errors=str(e))


class SendVerifyLinkToDeveloper(generics.CreateAPIView):
    # serializer_class = DeveloperDeleteSerializer

    def create(self, request, *args, **kwargs):
        try:
            developer_id = request.data.get('developer_id', None)
            dev = Developer.objects.filter(pk=developer_id, account__user__is_active=True).last()
            if dev:
                verify_obj = VerifyDetail.objects.create(user=dev.account.user, verify_link_sent_at=timezone.now())
                to_emails = ["ashwin@thoughtwin.com"]
                from_email = "ashwin@thoughtwin.com"
                extra_params = {}
                extra_params['name'] = f"{dev.account.user.first_name} {dev.account.user.last_name} " # Developer's name
                extra_params['verify_link'] = f"{BACKEND_URL}auth/verify/{verify_obj.token}/"
                gateway_email.send_email(
                    from_email=from_email,
                    to_emails=to_emails,
                    template_name="VERIFY_DETAIL",
                    extra_params=extra_params
                )
                return response_data(200, "success", data={}, errors=None)
            else:
                return response_data(400, "failed", data={}, errors=None)
        except Exception as e:
            print(e)
            return response_data(500, "failed", data={}, errors=str(e))

class VerifyDetailTokenView(View):
    def get(self, request, token):
        try:
            verify_detail = VerifyDetail.objects.filter(token=token, is_verified=False).last()
            if verify_detail:
                user = verify_detail.user
                context = {'user':user , 'token' : verify_detail.token }
                return render(request, "verify-detail.html", context)
            else:
                return render(request, "invalid-token.html", context={'message' : 'You have already submitted your details.'})
        except Exception as e:
            return render(request, "invalid-token.html")

    def post(self, request, token):
        try:
            verify_detail = VerifyDetail.objects.filter(token=token, is_verified=False).last()
            if verify_detail:
                dob = request.POST.get('dateofbirth', None)
                mob = request.POST.get('mobile', None)
                Developer.objects.filter(account__user=verify_detail.user).update(dob=dob)
                User.objects.filter(pk=verify_detail.user.pk).update(mobile_number=mob)
                verify_detail.is_verified=True
                verify_detail.verified_at=timezone.now()
                verify_detail.save()
            return render(request, "thankyou.html")
        except Exception as e:
            return render(request, "thankyou.html")