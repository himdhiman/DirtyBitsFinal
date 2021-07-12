from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import string, random


class DateTime(models.Model):
    dateTime = models.DateTimeField(null=True, blank = True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_Name, last_Name, password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_Name = first_Name,
            last_Name = last_Name,
        )
        user.access_token = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)))
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, first_Name, last_Name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_Name = first_Name,
            last_Name = last_Name,
            password = password,
        )
        user.access_token = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)))
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name = "email", unique = True, max_length = 60)
    first_Name = models.CharField(max_length = 20)
    last_Name = models.CharField(max_length = 20)
    access_token = models.TextField(blank=True, null=True, default="NA")
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



class Tag(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Problem(models.Model):
    choose = (
        ("E", "Easy"),
        ("M", "Medium"),
        ("H", "Hard"),
    )

    title = models.CharField(max_length = 100)
    description = models.TextField()
    note = models.TextField(blank = True, null = True)
    tags = models.ManyToManyField(Tag)
    level = models.CharField(max_length = 20, choices = choose)
    accuracy = models.IntegerField()
    totalSubmissions = models.IntegerField()
    sampleTc = models.IntegerField()
    totalTC = models.IntegerField()
    createdAt = models.DateField()
    memoryLimit = models.IntegerField(null = True, blank = True, default=0)
    timeLimit = models.IntegerField(null = True, blank = True, default=0)


    def __str__(self):
        return self.title


class UploadTC(models.Model):
    name = models.ForeignKey(to = "Problem", on_delete = models.CASCADE)
    testcases = models.FileField(upload_to = "tempTC/", blank = True, null = True)

class Submission(models.Model):
    LANGUAGE_CODE = (
        ('CP', 'CPP'),
        ('JV', 'JAVA'),
        ('P3', 'PYTHON 3'),
        ('P2', 'PYTHON 2'),
        ('JS', 'JAVASCRIPT')
    )
    STATUS_CODE = (
        ('Q', 'QUEUED'),
        ('R', 'RUNNING'),
        ('AC', 'ACCEPTED'),
        ('CE', 'COMPILATION ERROR'),
        ('WA', 'WRONG ANSWER'),
        ('RE', 'RUNTIME ERROR')
    )
    userId = models.IntegerField(blank = False)
    problemId = models.IntegerField(blank = False)
    language = models.CharField(max_length = 2, choices = LANGUAGE_CODE)
    code = models.TextField(blank = True)
    status = models.CharField(max_length = 2, choices = STATUS_CODE)
    error = models.TextField(blank = True)
    inputGiven = models.TextField(blank = True)
    outputGen = models.TextField(blank = True) 
    testCasesPassed = models.CharField(max_length = 15, blank = True)

    def __str__(self):
        return str(self.pk)





