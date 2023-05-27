from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **other_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        user = self.model(email=self.normalize_email(email), username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)
        
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **other_fields
        )

        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        EDITOR = "EDITOR", _("Editor")
        OPERATOR = "OPERATOR", _("Operator")
        STAFF = "STAFF", _("Staff")

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STAFF)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def role_name(self):
        return self.get_role_display

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
        

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ADMIN)
    

class EditorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EDITOR)


class OperatorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ADMIN)
    

class Editor(User):
    base_role = User.Role.EDITOR
    editors = EditorManager()

    class Meta:
        proxy = True


class Admin(User):
    base_role = User.Role.ADMIN
    admins = AdminManager()

    class Meta:
        proxy = True


class Operator(User):
    base_role = User.Role.OPERATOR
    operators = OperatorManager()

    class Meta:
        proxy = True

