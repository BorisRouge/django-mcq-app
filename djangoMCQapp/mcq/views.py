from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from .models import Answer, Question, QuestionSet, Users, UserAnswer, TestResult
from .forms import UserForm


class Register(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/register.html",
                      context={"form": form})

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.create_user(username, email, password)
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful")
        login(request, user)
        return redirect ("catalog")


class Login(View):
    def get(self, request):
        form = UserForm()
        return render(request, "mcq/login.html",
                      context={"form": form})

    def post(self, request):
        print(list(request.POST.items()))
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(email=email, password=password)
        if user is not None: # TODO: actions if the credentials are invalid
            login(request, user)
            return redirect("catalog")


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
            print(test_result)
            return redirect(test_result.first().get_absolute_url())
        context = {'question': question,
                   'answers': question.answers(), }
        return render(request, 'mcq/question.html', context)

    def post(self, request):
        pass  # TODO: gotta have a user first. The user must have the archive of tests.
              # TODO: back to catalog button


class SubmitAnswer(View):
    def get(self, request, question_id):
        answers = request.GET.getlist('answer')
        for answer_id in answers:
            user_answer, created = UserAnswer.objects.get_or_create(
                answer_id=answer_id,
                user_id=request.user.id,
                question_id=question_id)  # TODO: Check uniqueness and switch to next if existing. If query.exists().
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


class ResultView(View): # TODO: Make the template.
    def get(self, request, question_set):
        test_result = get_object_or_404(TestResult,
                                        user=request.user,
                                        question_set=question_set)
        context = {
            'total_answers': test_result.total_answers,
            'correct_answers': test_result.correct_answers,
            'ratio': test_result.ratio,
        }
        return render(request, 'mcq/result.html', context)