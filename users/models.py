from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

# Create your models here.
class Department(TimeStampedModel):
    department = models.CharField(max_length=500)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Department")

    def __str__(self):
        return self.department


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """Create and save a regular User with the given username and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    """
    Default custom user model for loom centric  Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    username = models.CharField(_("username"), unique=True, max_length=150,)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    user_role = models.CharField(max_length=50, default="Admin")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    objects = UserManager()


class Feedback(TimeStampedModel):
    feedback = models.CharField(max_length=500)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='department_manager')
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_employee')

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedback")

    def __str__(self):
        return self.Feedback