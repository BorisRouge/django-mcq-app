from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Users(User):
    pass


class QuestionSet(models.Model):
    name = models.TextField(max_length=256, default='Набор тестов')

    def __str__(self):
        return self.name

    def get_questions(self):
        return Question.objects.filter(question_set=self.id)

    def get_initial_question(self):
        return Question.objects.filter(
        question_set=self.id).first().get_absolute_url()


class Question(models.Model):
    question = models.TextField(max_length=256)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    def answers(self):
        return Answer.objects.filter(question=self.id)


class Answer(models.Model):
    answer = models.CharField(max_length=128)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

    def question_id(self):
        return self.question

    def is_correct(self):
        return self.correct

class UserAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def get_next_question(self):
        """Возвращает URL следующего в наборе вопроса
        или None, если вопросов больше нет."""
        answered_questions = Question.objects.filter(
            useranswer__user=self.user)
        question_set = Question.objects.filter(
            question_set=self.question.question_set)
        next_question = question_set.difference(answered_questions).first()
        if next_question is not None:
            return next_question.get_absolute_url()
        return None


class TestResult(models.Model): # Updated when retaken?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    total_answers = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    ratio = models.IntegerField(default=0)

    def set_results(self):
        self.total_answers = UserAnswer.objects.filter(
            question__question_set=self.question_set,
            user=self.user).count()
        self.correct_answers = UserAnswer.objects.filter(
            question__question_set=self.question_set,
            user=self.user,
            answer__correct=True).count()
        self.ratio = (self.correct_answers/self.total_answers)*100

    def get_absolute_url(self):
        return reverse('result', kwargs={'question_set': self.question_set.id})

