from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'master/countries', views.CountryViewSet, basename='country')
router.register(r'master/states', views.StateViewSet, basename='state')
router.register(r'master/cities', views.CityViewSet, basename='city')
router.register(r'master/currencies', views.CurrencyViewSet, basename='currency')
router.register(r'master/languages', views.LanguageViewSet, basename='language')
router.register(r'master/designations', views.DesignationViewSet, basename='designation')
router.register(r'master/departments', views.DepartmentViewSet, basename='department')
router.register(r'master/categories', views.CategoryViewSet, basename='category')
router.register(r'master/universities', views.UniversityViewSet, basename='university')
router.register(r'master/institutes', views.InstituteViewSet, basename='institute')
router.register(r'master/course', views.ProgramListCreateView, basename='program')

app_name = 'accounts'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.LoginView.as_view(), name='login'),  # Updated path
    path('auth/send-otp/', views.SendOTPView.as_view(), name='send-otp'),  # Updated path
    path('auth/verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),  # Updated path
    path('auth/request-password-reset/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('auth/verify-reset-otp/', views.VerifyResetOTPView.as_view(), name='verify-reset-otp'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('master/tables/', views.MasterTableListView.as_view(), name='master-tables'),
]
