from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class DateTime(models.Model):
    dateTime = models.DateTimeField(null=True, blank = True)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_Name, last_Name, password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_Name = first_Name,
            last_Name = last_Name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, first_Name, last_Name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_Name = first_Name,
            last_Name = last_Name,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user



class CustomUser(AbstractBaseUser):

    email = models.EmailField(verbose_name = "email", unique = True, max_length = 60)
    first_Name = models.CharField(max_length = 20)
    last_Name = models.CharField(max_length = 20)
    joining_Date = models.DateField(auto_now = True, verbose_name = "date joined")
    last_login = models.DateField(auto_now = True, verbose_name = "last login")
    solved = models.IntegerField(blank=True, null=True, default=0)
    partiallySolved = models.IntegerField(blank=True, null=True, default=0)
    attemped = models.IntegerField(blank=True, null=True, default=0)
    score = models.IntegerField(blank=True, null=True, default=0)
    rank = models.IntegerField(blank=True, null=True, default=0)
    problemsSolved = models.TextField(blank=True, null=True)
    problemPartiallySolved = models.TextField(blank=True, null=True)
    dateTime = models.ManyToManyField(DateTime)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_Name', 'last_Name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True





