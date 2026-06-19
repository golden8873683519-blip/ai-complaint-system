from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import (admin_dashboard, analytics_api)

urlpatterns = [

    # =========================
    # AUTH
    # =========================
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # =========================
    # DASHBOARD ROUTER (MAIN)
    # =========================
    path('dashboard/', views.dashboard, name='dashboard'),

    # =========================
    # ROLE DASHBOARDS
    # =========================
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('department-dashboard/', views.department_dashboard,
         name='department_dashboard'),
    # =========================
    # COMPLAINT SYSTEM
    # =========================
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('register-complaint/', views.register_complaint,
         name='register_complaint'),
    path('complaint/<int:id>/', views.complaint_detail, name='complaint_detail'),
    path('track-complaint/', views.track_complaint, name='track_complaint'),
    path('complaint-analytics/', views.complaint_analytics,
         name='complaint_analytics'),
    path('analytics-api/', analytics_api, name='analytics_api'),
    path("complaint-success/", views.complaint_success, name="complaint_success"),


    # =========================
    # ADMIN ACTIONS
    # =========================
    path('assign-complaint/<int:pk>/',
         views.assign_complaint, name='assign_complaint'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),

    # =========================
    # DROPDOWNS (AJAX)
    # =========================
    path('get-categories/<int:dept_id>/',
         views.get_categories, name='get_categories'),
    path('get-subcategories/<int:cat_id>/',
         views.get_subcategories, name='get_subcategories'),

    # =========================
    # PROFILE
    # =========================
    path('profile/', views.profile_view, name='profile'),

    # =========================
    # FEEDBACK SYSTEM
    # =========================
    path('feedback/<int:complaint_id>/',
         views.submit_feedback, name='submit_feedback'),

    # =========================
    # EXPORTS
    # =========================
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/csv/', views.export_csv, name='export_csv'),

    # =========================
    # USER VERIFICATION
    # =========================
    path('check-user/', views.check_user, name='check_user'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # =========================
    # OTP
    # =========================
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # =========================
    # PASSWORD RESET
    # =========================
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
