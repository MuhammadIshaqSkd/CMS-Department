from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.forms import UserForm, DepartmentForm, FeedbackForm
from django.contrib.auth.decorators import login_required
from users.models import Department, Feedback
# Create your views here.
from django.http import JsonResponse


User = get_user_model()


class AdminDashboard(LoginRequiredMixin, View):
    login_url = '/login'

    @staticmethod
    def get(request):
        if request.user.user_role != "Admin":
            messages.error(request, "Access denied.")
            return redirect('/')

        users = User.objects.all()
        departments = Department.objects.all()  # Get all departments
        feedbacks = Feedback.objects.select_related('manager', 'employee')  # Fetch feedback data with related fields

        return render(request, 'admin_dashboard.html', {
            "users": users,
            "departments": departments,  # Add departments to the context
            "feedbacks": feedbacks,  # Add feedbacks to the context
        })



@login_required
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # Save the user if the form is valid
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('admin_dashboard')
        else:
            # If the form is not valid, display errors
            messages.error(request, 'There was an error creating the user.')
    else:
        form = UserForm()

    return render(request, 'add_user.html', {'form': form})


@login_required
def delete_user(request, user_id):
    if request.user.user_role != "Admin":
        messages.error(request, "Access denied.")
        return redirect("home")

    user = get_object_or_404(User, id=user_id)
    if user.user_role == "Admin":
        messages.error(request, "Cannot delete another admin.")
        return redirect("admin_dashboard")

    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("admin_dashboard")



@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    departments = Department.objects.all()  # Fetch all departments

    if request.method == "POST":
        new_role = request.POST.get('user_role')
        new_department = request.POST.get('department')

        # Ensure that role and department are valid (you can add custom validation if needed)
        if new_role in ['Manager', 'Employee']:
            user.user_role = new_role
        if new_department:
            user.department = Department.objects.get(id=new_department)

        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('admin_dashboard')  # Redirect after successful update

    return render(request, 'edit_user.html', {'user': user, 'departments': departments})


@login_required
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('admin_dashboard')  # Redirect to the department list page
        else:
            messages.error(request, 'There was an error adding the department.')
    else:
        form = DepartmentForm()

    return render(request, 'add_department.html', {'form': form})


# Edit Department
@login_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'There was an error updating the department.')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'edit_department.html', {'form': form, 'department': department})


# Delete Department
@login_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, 'Department deleted successfully!')
    return redirect('admin_dashboard')


class FeedbackListView(View):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        return render(request, 'admin_dashboard.html', {'feedbacks': feedbacks})

class FeedbackCreateView(View):
    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback added successfully!")
        return redirect('admin_dashboard')

@login_required
def edit_feedback(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback-id')
        feedback_instance = get_object_or_404(Feedback, id=feedback_id)

        # Only allow edit if the user is the manager or admin
        if request.user != feedback_instance.manager and not request.user.is_staff:
            return JsonResponse({"success": False, "message": "You are not authorized to edit this feedback."}, status=403)

        # Get the feedback details from the POST data
        feedback_text = request.POST.get('feedback')
        manager_id = request.POST.get('manager')
        employee_id = request.POST.get('employee')

        # Update the feedback instance
        feedback_instance.feedback = feedback_text
        feedback_instance.manager_id = manager_id
        feedback_instance.employee_id = employee_id
        feedback_instance.save()

        return JsonResponse({"success": True, "message": "Feedback updated successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

class FeedbackDeleteView(View):
    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        feedback.delete()
        messages.success(request, "Feedback deleted successfully!")
        return redirect('admin_dashboard')
