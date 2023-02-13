from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models import Count
# Create your models here.


class MyUser(AbstractUser):
    phone=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profilepics",null=True)

class Questions(models.Model):
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    @property
    def fetch_answers(self):
        answers=self.answers_set.all().annotate(u_count=Count('upvote')).order_by('-u_count')
        return answers

    def __str__(self):
        return self.description

class Answers(models.Model):
    questions=models.ForeignKey(Questions, on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True)
    upvote=models.ManyToManyField(MyUser,related_name="upvote")
