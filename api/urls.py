from accounts.views import AdminRegistrationViewSet, AdministratorProfileAPIView, CustomerProfileAPIView, CustomerRegistrationViewSet, LoginViewSet, PasswordResetTokenCheck, RefreshViewSet, RequestPasswordResetEmail, SetNewPasswordAPIView, VerifyEmail
from inventory.views import CategoryAPIView, ProductAPIView, RatingAPIVIew
from orders.views import OrderAPIVIew
from rest_framework.routers import SimpleRouter
from django.urls import path
from django.views.generic import TemplateView


app_name = "api"
routes = SimpleRouter()
#Accounts
routes.register("login", LoginViewSet, basename="login")
routes.register("register", CustomerRegistrationViewSet,
                basename="register")
routes.register("admin/signup", AdminRegistrationViewSet,
                basename="admin-register")
routes.register('auth/refresh', RefreshViewSet, basename="auth-refresh")
routes.register('password-reset', RequestPasswordResetEmail,
                basename='requestPasswordReset')
routes.register('password-reset-complete', SetNewPasswordAPIView,
                basename="password-reset-complete")
routes.register("customer/profile", CustomerProfileAPIView,
                basename="customer-profile")
routes.register("admin/profile", AdministratorProfileAPIView,
                basename="admin-profile")

#Products routes
routes.register("products", ProductAPIView, basename="products")
routes.register("category", CategoryAPIView, basename="category")
routes.register("rating", RatingAPIVIew, basename="rating")

# Order routes
routes.register("orders", OrderAPIVIew, basename="orders")

urlpatterns  = [
    *routes.urls,
    path('activate/', VerifyEmail,
        name='email-verify'),
    path('password-reset/<uidb64>/<token>', PasswordResetTokenCheck,
        name='password-reset-confirm'),
    path('password-reset-successful/',
        TemplateView.as_view(
            template_name="accounts/password_reset_success.html"),
            name="passwordResetSuccess"
        ),
]