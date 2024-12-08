from django.urls import path

from dashboard.views import (
    AdminDashboard,

)
from . import views
from django.contrib.auth import views as auth_views
from .views import FeedbackListView, FeedbackCreateView, FeedbackEditView, FeedbackDeleteView

urlpatterns = [
    path("", AdminDashboard.as_view(), name='admin_dashboard'),  # Add the name here
    path("dashboard/create/", views.create_user, name="create_user"),
    path("dashboard/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("dashboard/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path('logout/', views.logout, name="logout"),  # Redirect to login page after logout

    path('departments/add/', views.add_department, name='add_department'),  # Add Department URL
    path('departments/edit/<int:department_id>/', views.edit_department, name='edit_department'),  # Edit Department URL
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    # Delete Department URL

    # Feedback URLs
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),  # List feedbacks
    path('feedbacks/add/', FeedbackCreateView.as_view(), name='add_feedback'),  # Create feedback
    path('feedbacks/edit/<int:pk>/', FeedbackEditView.as_view(), name='edit_feedback'),  # Edit feedback
    path('feedbacks/delete/<int:pk>/', FeedbackDeleteView.as_view(), name='delete_feedback'),  # Delete feedback

    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goals/add/', views.GoalCreateView.as_view(), name='add_goal'),
    path('goals/edit/<int:pk>/', views.GoalEditView.as_view(), name='edit_goal'),
    path('goals/delete/<int:pk>/', views.GoalDeleteView.as_view(), name='delete_goal'),

]
