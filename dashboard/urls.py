from django.urls import path

from dashboard.views import (
    AdminDashboard,

)

urlpatterns = [
    path("", AdminDashboard.as_view(), name='admin_dashboard'),  # Add the name here
]
