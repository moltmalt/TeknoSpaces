from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminManager(BaseUserManager):
    def create_user(self, username, first_name=None, last_name=None, password=None):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name=None, last_name=None,password=None):
        user = self.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AdminManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'


class Space(models.Model):
    space_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    seating_capacity = models.PositiveIntegerField()
    has_air_conditioner = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    has_television = models.BooleanField(default=False)

    # ForeignKey to track which admin added the space
    added_by = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='spaces_added', null=True, blank=True)

    def __str__(self):
        return self.space_title
