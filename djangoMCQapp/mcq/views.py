from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Answer, Question, QuestionSet

#from .forms import QuestionForm
# Create your views here.


class QuestionView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        context = {'question': question,
                   'answers': question.answers(),}
        return render(request, 'mcq/test.html', context)

    def post(self, request):
        pass # TODO: gotta have a user first. The user must have the archive of tests.
