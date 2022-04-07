from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('<slug:slug>/profile', views.ProfileView.as_view(), name="profile"),
    path('<slug:slug>/profile/edit', views.EditProfileView.as_view(), name="edit_profile")
]
