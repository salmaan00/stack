from django.contrib import admin

# Register your models here.
from questions.models import MyUser

admin.site.register(MyUser)