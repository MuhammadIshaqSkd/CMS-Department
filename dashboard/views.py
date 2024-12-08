from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.forms import UserForm, DepartmentForm, FeedbackForm, GoalForm
from django.contrib.auth.decorators import login_required
from users.models import Department, Feedback, Goal
# Create your views here.


User = get_user_model()


class AdminDashboard(LoginRequiredMixin, View):
    login_url = '/login'

    @staticmethod
    def get(request):
        users = User.objects.all()
        departments = Department.objects.all()  # Get all departments
        feedbacks = Feedback.objects.all() # Fetch feedback data with related fields
        goals = Goal.objects.all()  # Fetch all goals
        if request.user.user_role == "Manager":
            feedbacks = feedbacks.filter(manager=request.user)
            goals = goals.filter(employee__department=request.user.department)
        if request.user.user_role == "Employee":
            feedbacks = feedbacks.filter(employee=request.user)
            goals = goals.filter(employee__department=request.user.department)
        return render(request, 'admin_dashboard.html', {
            "users": users,
            "departments": departments,  # Add departments to the context
            "feedbacks": feedbacks,  # Add feedbacks to the context
            "goals": goals,  # Add goals to the context
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
        departments = Department.objects.all()  # Fetch all departments
        form = UserForm()

    return render(request, 'add_user.html', {'form': form,'departments':departments})


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
        return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


class FeedbackCreateView(View):
    def get(self, request):
        form = FeedbackForm()
        req_user = request.user.user_role
        # Fetch users who can be managers or employees
        managers = User.objects.filter(user_role="Manager")  # or based on your own filter criteria
        employees = User.objects.filter(user_role="Employee")
        if req_user == 'Manager':
            employees = employees.filter(department=request.user.department)
        # or based on your own filter criteria
        return render(request, 'feedback_form.html', {
            'form': form,
            'managers': managers,
            'employees': employees,
            'req_user':  req_user,
        })

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback created successfully!")
            return redirect('admin_dashboard')
        # Fetch managers and employees again for validation failure
        managers = User.objects.filter(user_role="Manager")  # or based on your own filter criteria
        employees = User.objects.filter(user_role="Employee")  # or based on your own filter criteria

        return render(request, 'feedback_form.html', {
                'form': form,
                'managers': managers,
                'employees': employees,
            })


class FeedbackEditView(View):
    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        form = FeedbackForm(instance=feedback)
        # Fetch users who can be managers or employees
        managers = User.objects.filter(user_role="Manager")  # or based on your own filter criteria
        employees = User.objects.filter(user_role="Employee")  # or based on your own filter criteria
        return render(request, 'feedback_form.html', {
                'form': form,
                'managers': managers,
                'employees': employees,
                'feedback': feedback,
            })

    def post(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully!")
            return redirect('admin_dashboard')
        # Fetch managers and employees again for validation failure
        managers = User.objects.filter(user_role="Manager")  # or based on your own filter criteria
        employees = User.objects.filter(user_role="Employee")  # or based on your own filter criteria

        return render(request, 'feedback_form.html', {
            'form': form,
            'managers': managers,
            'employees': employees,
            'feedback': feedback,
        })


class FeedbackDeleteView(View):
    def get(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        feedback.delete()
        messages.success(request, "Feedback deleted successfully!")
        return redirect('admin_dashboard')  # Redirect to the feedback list page


class GoalListView(View):
    def get(self, request):
        goals = Goal.objects.all()

        return render(request, 'goal_list.html', {'goals': goals})


class GoalCreateView(View):
    def get(self, request):
        form = GoalForm()
        employees = User.objects.filter(user_role="Employee")  # or based on your own filter criteria
        if request.user.user_role == 'Manager':
            employees = employees.filter(department= request.user.department)

        return render(request, 'goal_form.html', {'form': form, 'employees': employees})

    def post(self, request):
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal created successfully!")
            return redirect('admin_dashboard')
        employees = User.objects.all()  # Adjust based on employee filter logic
        return render(request, 'goal_form.html', {'form': form, 'employees': employees})


class GoalEditView(View):
    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalForm(instance=goal)
        employees = User.objects.filter(user_role="Employee")  # or based on your own filter criteria
        return render(request, 'goal_form.html', {'form': form, 'employees': employees, 'goal': goal})

    def post(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated successfully!")
            return redirect('goal_list')
        employees = User.objects.all()  # Adjust based on employee filter logic
        return render(request, 'goal_form.html', {'form': form, 'employees': employees, 'goal': goal})


class GoalDeleteView(View):
    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        goal.delete()
        messages.success(request, "Goal deleted successfully!")
        return redirect('goal_list')

@login_required
def logout(request):
    return redirect('/')
