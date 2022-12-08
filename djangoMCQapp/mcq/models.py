from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User(User):
    pass


class QuestionSet(models.Model):
    name = models.TextField(max_length=256, default='Набор тестов')

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.TextField(max_length=256)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def answers(self):
        return Answer.objects.filter(question=self.id)

class Answer(models.Model):
    answer = models.CharField(max_length=128)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer

# class TestResult ???
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
