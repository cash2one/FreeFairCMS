from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class EditorManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None):
        user = self.model(
            email=email,
            is_superuser=True,
            role=self.model.ADMIN
        )
        user.set_password(password)
        user.save()


class Editor(AbstractBaseUser, PermissionsMixin):
    """
    User model that also includes different roles that corresponding to different permission levels.
        Admin: Full Publishing and Editing Access
        Editor: Can Edit and Submit changes for specific states, but can't publish those changes
        Publisher: Can Edit and Publish state changes, without specific 
    """
    ADMIN = 'A'
    EDITOR = 'E'
    PUBLISHER = 'P'

    EDITOR_ROLES = (
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
    )
    
    role = models.CharField(
        max_length=1,
        choices=EDITOR_ROLES,
        default=ADMIN,
        blank=False
    )

    email = models.EmailField('email address', unique=True)
    is_active = models.BooleanField(default=True)

    @property
    def is_staff(self):
        return self.role == self.ADMIN

    @property
    def username(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    objects = EditorManager()
