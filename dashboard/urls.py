from django.urls import path

from dashboard.views import (
    AdminDashboard,

)
from . import views
from django.contrib.auth.views import LogoutView
from .views import FeedbackListView, FeedbackCreateView, FeedbackDeleteView

urlpatterns = [
    path("", AdminDashboard.as_view(), name='admin_dashboard'),  # Add the name here
    path("dashboard/create/", views.create_user, name="create_user"),
    path("dashboard/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("dashboard/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),

    path('departments/add/', views.add_department, name='add_department'),  # Add Department URL
    path('departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),  # Edit Department URL
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    # Delete Department URL

    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedbacks/add/', FeedbackCreateView.as_view(), name='add_feedback'),
    path('edit_feedback/', views.edit_feedback, name='edit_feedback'),
    path('feedbacks/delete/<int:pk>/', FeedbackDeleteView.as_view(), name='delete_feedback'),

]
