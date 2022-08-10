import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import File
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.db.models import Q, query
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                    smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


from accounts.models import User, Administrator, Customer
from accounts.permissions import IsAdministrator, IsCustomer
from accounts.send_mails import send_activation_mail, send_password_reset_email
from accounts.serializers import (AdministratorProfileSerializer, CustomerProfileSerializer,
                                LoginSerializer, RegisterSerializer,
                                ResetPasswordEmailRequestSerializer,
                                SetNewPasswordSerializer, UserSerializer)


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomerRegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = "Customer"
        user.is_active = False
        user.save()
        Customer.objects.update_or_create(user=user)
        user_data = serializer.data
        send_activation_mail(user_data, request)

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response({
            "user": serializer.data,
            "refresh": res['refresh'],
                        "token": res['access']
                        }, status=status.HTTP_201_CREATED)


class AdminRegistrationViewSet(ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    http_method_names = ['post',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = "Administrator"
        user.is_active = False
        user.save()
        Administrator.objects.update_or_create(user=user)
        user_data = serializer.data
        send_activation_mail(user_data, request)

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response({
            "user": serializer.data,
            "refresh": res['refresh'],
                        "token": res['access']
                        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


def VerifyEmail(request):
    token = request.GET.get("token")
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256"
        )
        user = User.objects.get(id=payload['user_id'])
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request,
                            "Account was Successfully Verified.")
        else:
            messages.info(request,
                            """Your Account has already been activated.
                            You can now login and 
                            write the Tasks you do.
                            """)
    except jwt.ExpiredSignatureError as identifier:
        messages.warning(request,
                        "The Activation Link Expired!")
    except jwt.exceptions.DecodeError as identifier:
        messages.warning(request, "Invalid Activation Link!")
    context = {
    }
    return render(request, "accounts/verify.html", context)


# Password Reset


class RequestPasswordResetEmail(ModelViewSet):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        # email = request.data["email"]
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            if user.is_active:
                send_password_reset_email(user, request)
            return Response(
                {"Success": "We have emailed you a link to reset your password"},
                status=status.HTTP_200_OK
            )
        return Response({"Success": "Password Reset Link was sent to your email."})


def PasswordResetTokenCheck(request, uidb64, token):
    try:
        id = smart_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(
                request,
                "Password Reset Link is no longer valid, please request a new one.")
    except DjangoUnicodeDecodeError as identifier:
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(
                request,
                "Password is no longer valid, please request a new one.")
    context = {
        "uidb64": uidb64,
        "token": token,
    }
    return render(request, "accounts/password_reset.html", context)


class SetNewPasswordAPIView(ModelViewSet):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post', "get"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            password = request.data["password"]
            password_confirmation = request.data["password_confirmation"]
            token = request.data["token"]
            uidb64 = request.data["uidb64"]
            if (password and password_confirmation
                    and password != password_confirmation):
                raise serializers.ValidationError(
                    {"Error": ("Password don\'t match!")}
                )
            else:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed(
                        "The Reset Link is Invalid",
                        401,
                    )
                else:
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"Success": "Password reset successful"},
                        status=status.HTTP_201_CREATED)
        except Exception as e:
            raise AuthenticationFailed(
                "The Reset Link is Invalid", 401)
        return Response(serializer.data)
#Profiles


class CustomerProfileAPIView(ModelViewSet):
    """
    Customer Profile API View
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    http_method_names = ["get", "put", "patch"]

    def get_queryset(self):
        user = self.request.user
        customerQuery = Customer.objects.filter(
            Q(user=user)
        )
        return customerQuery
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, may=False)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                        partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        userSerializer = UserSerializer(
            request.user, data=request.data["user"],
            partial=True
        )
        userSerializer.is_valid(raise_exception=True)
        instance.user.username = userSerializer.validated_data["username"]
        instance.user.full_name = userSerializer.validated_data["full_name"]
        instance.user.phone = userSerializer.validated_data["phone"]
        instance.user.save()
        userSerializer.save()
        return Response(
            serializer.data, status=status.HTTP_202_ACCEPTED
        )


class AdministratorProfileAPIView(ModelViewSet):
    """
    Administrator Profile API View
    """
    serializer_class = AdministratorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        user = self.request.user
        adminQuery = Administrator.objects.filter(
            Q(user=user)
        )
        return adminQuery
    
    def retieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        userSerializer = UserSerializer(
            request.user, data=request.data["user"]
        )
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()
        return Response(
            serializer.data, status=status.HTTP_202_ACCEPTED
        )