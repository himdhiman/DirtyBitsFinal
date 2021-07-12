from django.contrib import admin
from api import models

admin.site.register([
    models.CustomUser,
    models.Tag,
    models.Problem,
    models.UploadTC,
    models.Submission
    ])
