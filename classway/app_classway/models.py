from django.db import models
from account.models import User

# Create your models here.


class Class(models.Model):
    # class_id = models.IntegerField()
    class_name = models.CharField(max_length=100)
    class_subject = models.CharField(max_length=200)
    class_code = models.CharField(max_length=8)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_admin = models.CharField(max_length=100)


class Question(models.Model):
    qn_desc = models.TextField(max_length=500)
    qn_marks = models.IntegerField()
    qn_date = models.DateTimeField(auto_now_add=True, blank=True)
    qn_deadline = models.DateTimeField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)


class Answer(models.Model):
    ans_desc = models.TextField(max_length=10000)
    # ans_file = models.CharField(max_length=10)
    ans_date = models.DateTimeField(auto_now_add=True, blank=True)
    qn_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ans_marks = models.IntegerField()


class Enroll(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
