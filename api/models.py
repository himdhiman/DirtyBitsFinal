from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import string, random

class Submission(models.Model):
    problemId = models.IntegerField(blank = False)
    language = models.IntegerField(blank = False)
    code = models.TextField(blank = False)
    status = models.CharField(max_length=30,default="Queued")
    error = models.TextField(blank = True)
    input_Given = models.TextField(blank = True)
    output_Generated = models.TextField(blank = True) 
    test_Cases_Passed = models.IntegerField(blank = True)
    total_Test_Cases = models.IntegerField(blank = True)
    submission_Date_Time = models.DateTimeField(null=True, blank = True)

    def __str__(self):
        return str(self.id)

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
    questions_solved = models.IntegerField(blank=True, null=True, default=0)
    questions_partiallySolved = models.IntegerField(blank=True, null=True, default=0)
    questions_attemped = models.IntegerField(blank=True, null=True, default=0)
    score = models.IntegerField(blank=True, null=True, default=0)
    rank = models.IntegerField(blank=True, null=True, default=0)
    problems_Solved = models.TextField(blank=True, null=True)
    problems_Partially_Solved = models.TextField(blank=True, null=True)
    submissions = models.ManyToManyField(Submission, blank=True)
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
    sample_Tc = models.IntegerField()
    total_Tc = models.IntegerField()
    created_At = models.DateField(auto_now=True)
    memory_Limit = models.IntegerField(null = True, blank = True, default=5120)
    time_Limit = models.IntegerField(null = True, blank = True, default=1)


    def __str__(self):
        return self.title


class UploadTC(models.Model):
    name = models.ForeignKey(to = "Problem", on_delete = models.CASCADE)
    testcases = models.FileField(upload_to = "tempTC/", blank = True, null = True)







