from django import forms
from .models import User
from .models import Department, Feedback, Goal


from django.contrib.auth.hashers import make_password

class UserForm(forms.ModelForm):
    USER_ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]

    user_role = forms.ChoiceField(choices=USER_ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'user_role', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'manager', 'employee']


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal', 'employee', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
