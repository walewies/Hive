from django.urls import path
from . import views

app_name = "leaderboard"

urlpatterns = [
    path("daily/", views.DailyLeaderboard.as_view(), name="daily"),
    path("weekly/", views.WeeklyLeaderboard.as_view(), name="weekly"),
    path("monthly/", views.MonthlyLeaderboard.as_view(), name="monthly"),
    path("yearly/", views.YearlyLeaderboard.as_view(), name="yearly"),
    path("all-time/", views.AllTimeLeaderboard.as_view(), name="all_time"),
]