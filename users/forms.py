from django import forms
from .models import User
from .models import Department, Feedback


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



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'manager', 'employee']