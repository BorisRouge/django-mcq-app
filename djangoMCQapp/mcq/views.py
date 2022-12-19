from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from django.views import View
from .models import Question, QuestionSet, Users, UserAnswer, TestResult
from .forms import UserForm, LoginForm




class Register(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/register.html",
                      context={"form": form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid:
            form.save() # TODO: won't authenticate new user
            return redirect("catalog")
        else:
            messages.error(request, 'Что-то пошло не так')
            return redirect('register')

class Login(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/login.html",
                      context={"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid:
            user = authenticate(
                email=form['email'],
                password=form['password'])
            if user is not None:  # TODO: actions if the credentials are invalid
                login(request, user)
                return redirect("catalog")
            else:
                messages.error(request, 'Адрес или пароль не найдены')
                return redirect('login')
# TODO: Login won't log in with valid credentials.


class Catalog(View):
    def get(self, request):
        question_sets = QuestionSet.objects.all()
        return render(request,
               "mcq/catalog.html",
               {'question_sets':question_sets})


class QuestionView(View):

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        test_result = TestResult.objects.filter(
            user=request.user,
            question_set=question.question_set)
        if test_result.exists():
            return redirect(test_result.first().get_absolute_url())
        context = {'question': question,
                   'answers': question.answers(), }
        return render(request, 'mcq/question.html', context)


class SubmitAnswer(View):
    def get(self, request, question_id):
        answers = request.GET.getlist('answer')
        for answer_id in answers:
            user_answer, created = UserAnswer.objects.get_or_create(
                answer_id=answer_id,
                user_id=request.user.id,
                question_id=question_id)
        result = user_answer.get_next_question()
        if result is not None:
            return redirect(result)  # Might want to change where this method belongs.

        test_result = TestResult(
            user=request.user,
            question_set=QuestionSet.objects.get(
                pk=user_answer.question.question_set.id))
        test_result.set_results()
        test_result.save()
        return redirect(test_result.get_absolute_url())


class ResultView(View):
    def get(self, request, question_set):
        test_result = get_object_or_404(TestResult,
                                        user=request.user,
                                        question_set=question_set)
        context = {
            'incorrect_answers': test_result.total_answers-test_result.correct_answers,
            'correct_answers': test_result.correct_answers,
            'ratio': test_result.ratio,
        }
        return render(request, 'mcq/result.html', context)