from posixpath import basename
from accounts.views import AdminRegistrationViewSet, AdministratorProfileAPIView, CustomerProfileAPIView, CustomerRegistrationViewSet, LoginViewSet, PasswordResetTokenCheck, RefreshViewSet, RequestPasswordResetEmail, SetNewPasswordAPIView, VerifyEmail
from rest_framework.routers import SimpleRouter
from django.urls import path
from django.views.generic import TemplateView
