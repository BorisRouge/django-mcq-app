from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class User(User):
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
    #TODO: Priority in a set?
    #TODO: FSM or something like it
    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})

    def answers(self):
        return Answer.objects.filter(question=self.id)
        #TODO: might be redundant, see
        # https://docs.djangoproject.com/en/4.1/topics/db/queries/#lookups-that-span-relationships.
        # OR the question set should have a lookup method
        # to get the absolute url of the initial question.

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

    @staticmethod
    def next_question(question_id, user):
        # question_set = QuestionSet.objects.get(question__id=question_id)
        # #questions = question_set.get_questions()
        # questions =Question.objects.filter(
        #     question_set=question_set).exclude(=question_id)
        # print(questions)
        # index = questions.index(Question.objects.get(question_id))
        # try:
        #     return questions[index+1].get_absolute_url()
        # except IndexError:
        #     return UserAnswer.get_result()
    Question.objects.filter(pk=answer__question__id)


    @staticmethod
    def get_result(self):
        pass

# class TestResult ???
#   user = models.ForeignKey(User, on_delete=models.CASCADE)
