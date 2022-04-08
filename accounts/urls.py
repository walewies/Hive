from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('<slug:slug>/profile', views.ProfileView.as_view(), name="profile"),
    path('<slug:slug>/profile/edit', views.EditProfileView.as_view(), name="edit_profile"),
    path('<slug:slug>/change-password', views.ChangeUserPassword.as_view(), name="change_password"),
    path('<slug:slug>/validate-password-change', views.ValidateUserPassword, name="validate_password_change"),
    path('<slug:slug>/password-change-success', views.PasswordChangeSuccess.as_view(), name="password_change_success")
]
