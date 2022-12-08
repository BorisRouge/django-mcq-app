from django.shortcuts import render
from .models import Answer, Question, QuestionSet
#from .forms import QuestionForm
# Create your views here.


def test(request):
    question = Question.objects.get()
    context = {'question': question,
               'answers': question.answers(),}
    return render(request, 'mcq/test.html', context)
